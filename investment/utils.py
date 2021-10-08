from .models import *
from account.models import UserCard, Wallet
from account.utils import tokenize_user_card, debit_user_account
from modules.paystack import paystack_auto_charge, get_paystack_link, verify_paystack_transaction
import logging
from django.utils import timezone

log = logging.getLogger(__name__)


def can_pay_for_investment(investment):
    check_status = ['approved', 'ongoing', 'completed']
    if investment.status in check_status:
        return False
    return True


def create_or_update_investment_transaction(investment, amount, **kwargs):
    status = kwargs.get('status', 'pending')
    transaction_type = kwargs.get('transaction_type', 'investment')
    payment_method = kwargs.get('payment_method', 'paystack')
    reference = kwargs.get('reference', '')
    response = kwargs.get('response')
    user = investment.user

    transaction, created = InvestmentTransaction.objects.get_or_create(
        user=user, investment=investment, amount=amount, status=status
    )
    transaction.transaction_type = transaction_type
    transaction.payment_method = payment_method
    transaction.reference = reference
    transaction.response = response
    transaction.save()
    return transaction


def create_investment(profile, data):
    success = True
    response = "Investment created successfully"
    investment_id = data.get('investment_id')
    option_id = data.get('option_id')
    duration = data.get('duration_id')
    amount = data.get('amount')
    user = profile.user

    wallet, new_wallet = Wallet.objects.get_or_create(user=profile)
    if float(wallet.balance) < float(amount):
        return False, "Insufficient balance for this investment, please top-up your account"

    try:
        available_investment = AvailableInvestment.objects.get(id=investment_id)
        option = InvestmentOption.objects.get(id=option_id, available_investment=available_investment)
        duration = InvestmentDuration.objects.get(id=duration)
    except Exception as ex:
        return False, str(ex)

    investment, created = Investment.objects.get_or_create(
        user=profile, investment=available_investment, option=option, duration=duration, amount_invested=amount,
    )

    # check if user can pay for investment
    if can_pay_for_investment(investment) is False:
        return False, f"This investment is already {investment.status}"

    calc_roi = (amount * duration.percentage) / 100
    investment.return_on_invested = amount + calc_roi
    investment.number_of_month = duration.duration
    investment.number_of_days = duration.number_of_days
    investment.percentage = duration.percentage
    investment.save()

    reference = f"INV{investment.id}-{profile.id}"
    transaction = create_or_update_investment_transaction(
        investment=investment, amount=amount, reference=reference, response=response
    )

    user = debit_user_account(user=user, amount=amount)

    investment.start_date = timezone.now()
    investment.end_date = investment.start_date + timezone.timedelta(days=investment.number_of_days)
    investment.status = 'approved'
    investment.save()

    transaction.status = 'success'
    transaction.save()

    return success, investment


def approve_investment(investment_id, payment_gateway, payment_reference):
    success = True
    response = "Investment approved"
    status = 'pending'

    try:
        investment = Investment.objects.get(id=investment_id)
        amount = investment.amount_invested
    except Exception as ex:
        log.exception(str(ex))
        return False, str(ex)

    # check if user can pay for investment
    if can_pay_for_investment(investment) is False:
        return True, f"This investment is already {investment.status}"

    # Verify payment
    if payment_gateway == 'paystack':
        success, response = verify_paystack_transaction(payment_reference)
        if success is False:
            return False, response
        amount = response['amount']
        status = 'success'
        tokenize_user_card(response, 'paystack')

    create_or_update_investment_transaction(
        investment=investment, amount=amount, status=status, reference=payment_reference, response=response
    )

    if status == 'success':
        investment.start_date = timezone.now()
        investment.end_date = investment.start_date + timezone.timedelta(days=investment.number_of_days)
        investment.status = 'approved'
        investment.save()

    response = "Investment approved"
    return success, response


def investment_payment(user, data):
    success = True
    response = "Payment successful"
    investment_id = data.get('investment_id')
    card_id = data.get('card_id')
    gateway = reference = None

    try:
        investment = Investment.objects.get(id=investment_id, user=user)
    except Exception as ex:
        return False, str(ex)

    # check if user can pay for investment
    if can_pay_for_investment(investment) is False:
        return True, f"This investment is already {investment.status}"

    metadata = {
        'investment_id': investment.id,
        'payment_for': 'investment',
    }

    if card_id:
        try:
            card = UserCard.objects.get(id=card_id, user=user)
        except Exception as ex:
            return False, str(ex)

        if card.gateway == 'paystack':
            success, response = paystack_auto_charge(
                authorization_code=card.authorization_code,
                email=card.email,
                amount=investment.amount_invested,
                metadata=metadata
            )
            if success is True:
                gateway = card.gateway
                reference = response['data']['reference']
                investment_id = response['data']['metadata']['investment_id']

        success, response = approve_investment(investment_id, gateway, reference)

    if not card_id:
        callback_url = data.get('callback_url')
        gateway = data.get('gateway')

        if not callback_url:
            return False, "callback url is required"

        if not gateway:
            return False, "gateway is required"

        # get paystack payment link
        success, response = get_paystack_link(
            email=user.user.email, amount=investment.amount_invested, callback_url=callback_url, metadata=metadata,
        )
        if success is False:
            return success, response

    return success, response



