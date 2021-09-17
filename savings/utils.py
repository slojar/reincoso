import logging
from datetime import timedelta

from django.utils import timezone
from django.utils.timezone import datetime
from django.db.models import Sum

from account.models import UserCard
from modules.paystack import generate_payment_ref_with_paystack, paystack_auto_charge, verify_paystack_transaction, \
    get_paystack_link
from .models import *


def get_savings_analysis(profile):
    data = dict()
    total_savings = SavingTransaction.objects.filter(user=profile, status='success')
    total_savings = total_savings.aggregate(Sum('amount'))['amount__sum']
    data['total_savings_amount'] = total_savings
    return data


def create_instant_savings(savings_type, request):
    success = False
    response = ""
    amount = request.data.get('amount')
    gateway = request.data.get('gateway')
    payment_duration_id = request.data.get('payment_duration_id')
    card_id = request.data.get('card_id')

    email = request.user.email
    profile = request.user.profile

    try:
        payment_duration = Duration.objects.get(id=payment_duration_id)
    except Exception as ex:
        return False, f"{ex}"

    # Create/Update Saving Account
    saving, created = Saving.objects.get_or_create(user=profile, type=savings_type, amount=amount, status='pending')
    saving.type = savings_type
    saving.duration = payment_duration
    saving.amount = amount
    saving.total = amount
    saving.payment_day = timezone.now().day
    saving.last_payment = amount
    saving.last_payment_date = timezone.now()
    saving.next_payment_date = timezone.now()
    saving.auto_save = False
    saving.save()

    # Create saving transaction
    transaction_reference = generate_payment_ref_with_paystack(uid=f"SAV-{saving.id}")
    transaction, created = SavingTransaction.objects.get_or_create(user=profile, saving_id=saving.id, status='pending')
    transaction.payment_method = gateway
    transaction.reference = transaction_reference
    transaction.amount = amount
    transaction.save()

    metadata = {
        'transaction_id': transaction.id,
        'payment_for': 'savings',
        'reference': transaction_reference
    }

    if card_id:
        try:
            card = UserCard.objects.get(id=card_id)
            authorization_code = card.authorization_code
            success, response = paystack_auto_charge(authorization_code, email, amount, metadata=metadata)
            if not success:
                return False, response

            reference = response['data']['reference']

            success, response = verify_paystack_transaction(reference)
            if not success:
                return False, response

            saving.status = 'successful'
            saving.save()

            transaction.reference = reference
            transaction.status = 'success'
            transaction.response = response
            transaction.save()

            return True, "Payment Successful"

        except Exception as ex:
            logging.exception(f"{ex}")
            return False, f"{ex}"

    if not card_id:
        callback_url = request.data.get('callback_url')
        if not callback_url:
            callback_url = f"{request.scheme}://{request.get_host()}{request.path}"

        if gateway == 'paystack':
            success, response = get_paystack_link(email=email, amount=amount, callback_url=callback_url, metadata=metadata)
            return success, response

    return success, response


def create_auto_savings(savings_type, request):
    success = False
    response = ""
    amount = request.data.get('amount')
    payment_day = request.data.get('payment_day')
    gateway = request.data.get('gateway')
    payment_duration = request.data.get('payment_duration_id')
    card_id = request.data.get('card_id')
    email = request.user.email
    profile = request.user.profile

    try:
        payment_duration = Duration.objects.get(id=payment_duration)
    except Exception as ex:
        return False, f"{ex}"

    # Create/Update Saving Account
    saving, created = Saving.objects.get_or_create(user=profile, type=savings_type, amount=amount, status='pending')
    saving.duration = payment_duration
    saving.amount = amount
    saving.total = amount
    saving.payment_day = payment_day
    saving.last_payment = amount
    saving.last_payment_date = timezone.now()

    # Calculate next repayment date
    next_date = saving.last_payment_date + timedelta(days=saving.duration.number_of_day)
    saving.next_payment_date = next_date
    saving.auto_save = True
    saving.save()

    # Create saving transaction
    transaction_reference = generate_payment_ref_with_paystack(uid=f"SAV-{saving.id}")
    transaction, created = SavingTransaction.objects.get_or_create(user=request.user.profile, saving_id=saving.id, status='pending')
    transaction.payment_method = gateway
    transaction.reference = transaction_reference
    transaction.amount = amount
    transaction.save()

    metadata = {
        'transaction_id': transaction.id,
        'payment_for': 'savings',
        'reference': transaction_reference,
    }

    if card_id:
        try:
            card = UserCard.objects.get(id=card_id)
            authorization_code = card.authorization_code
            success, response = paystack_auto_charge(authorization_code, email, amount, metadata=metadata)
            if not success:
                return False, response

            reference = response['data']['reference']

            success, response = verify_paystack_transaction(reference)
            if not success:
                return False, response

            saving.status = 'successful'
            saving.save()

            transaction.reference = reference
            transaction.status = 'success'
            transaction.response = response
            transaction.save()

            return True, "Payment Successful"

        except Exception as ex:
            logging.exception(f"{ex}")
            return False, f"{ex}"

    if not card_id:
        callback_url = request.data.get('callback_url')
        if not callback_url:
            callback_url = f"{request.scheme}://{request.get_host()}{request.path}"

        if gateway == 'paystack':
            success, response = get_paystack_link(email=email, amount=amount, callback_url=callback_url,
                                                  metadata=metadata)
            return success, response

    return success, response


def auto_save_cron():
    ...


