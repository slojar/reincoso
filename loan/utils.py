import calendar
import decimal
from loan.models import *
from django.utils import timezone
from savings.models import SavingTransaction
from settings.models import LoanSetting
from account.models import UserCard, Guarantor
from django.db.models import Q
from modules.paystack import get_paystack_link, paystack_auto_charge, verify_paystack_transaction
from account.utils import tokenize_user_card


def get_loan_offer(profile):
    success = False
    response = ""
    loan_settings, created = LoanSetting.objects.get_or_create(site=Site.objects.get_current())
    savings_transaction = SavingTransaction.objects.filter(user=profile, status='success').first()

    if not savings_transaction:
        response = "Sorry, you are unable to get a loan right now. make sure you have saved for at least " \
                         "6 months before applying for loan."
        return success, response

    first_savings_date = savings_transaction.created_on
    last_six_month = timezone.now() - timezone.timedelta(days=loan_settings.eligibility_days)
    eligible = last_six_month >= first_savings_date

    if not eligible:
        response = "Sorry, you are unable to get a loan right now. make sure you have saved for at least " \
                         "6 months before applying for loan."
        return success, response

    balance = profile.wallet.balance

    if balance < 1000000:
        response = "Sorry, you are unable to get a loan right now. make sure you have saved up to One Million Naira " \
                   "(N1,000,000) before applying for loan."
        return success, response

    success = True
    response = round(balance * loan_settings.offer, 2)
    # response = round(savings_transaction.saving.total * loan_settings.offer, 2)
    return success, response


def get_loan_repayment_count(duration):
    repayment_day_count = 7

    if duration.basis == 'weekly':
        repayment_day_count = 7
    if duration.basis == 'monthly':
        year = timezone.now().year
        month = timezone.now().month
        next_month = calendar._nextmonth(year=year, month=month)[1]
        repayment_day_count = calendar.monthrange(year=timezone.now().year, month=next_month)[1]
    if duration.basis == 'yearly':
        year = timezone.now().year
        if not calendar.isleap(year=year):
            repayment_day_count = 365
        else:
            repayment_day_count = 366

    return repayment_day_count


def create_loan(request, profile, amount, duration):
    success = False
    repayment_day_of_the_week = request.data.get('repayment_day_of_the_week')
    repayment_day_of_the_month = request.data.get('repayment_day_f_the_month')

    if duration.basis == 'weekly':
        days_list = [str(day) for day in range(0, 8)]
        if not (repayment_day_of_the_week and str(repayment_day_of_the_week).lower() in days_list):
            response = f"You must select a repayment day of the week to continue"
            return success, response

    if duration.basis != 'weekly':
        days_list = [str(day) for day in range(0, 32)]
        if not (repayment_day_of_the_month and repayment_day_of_the_month in days_list):
            response = f"You must select a repayment day of the month to continue"
            return success, response

    success = True
    response = "Loan application successful, please wait while we process your loan"

    amount = decimal.Decimal(amount)
    loan = Loan.objects.create(user=profile)
    loan.amount = amount

    if repayment_day_of_the_week:
        loan.day_of_the_week = repayment_day_of_the_week
    if repayment_day_of_the_month:
        loan.payment_day = repayment_day_of_the_month

    loan.duration = duration
    loan.basis = duration.basis
    loan.basis_duration = duration.duration
    loan.number_of_days = duration.number_of_days
    loan.percentage = duration.percentage

    loan.percentage_amount = (amount * duration.percentage) / 100
    loan.amount_to_repay = amount + loan.percentage_amount
    loan.amount_to_repay_split = loan.amount_to_repay / loan.basis_duration
    loan.start_date = timezone.now()
    loan.end_date = loan.start_date + timezone.timedelta(days=duration.number_of_days)
    if duration.basis == 'weekly':
        loan.next_repayment_date = loan.start_date + timezone.timedelta(days=15)
    loan.next_repayment_date = loan.start_date + timezone.timedelta(days=get_loan_repayment_count(duration))
    loan.status = "processing"
    loan.save()

    return success, response


def can_get_loan(profile):
    success = False
    loan_settings = LoanSetting.objects.get(site=Site.objects.get_current())

    # check if user paid member fee
    if profile.paid_membership_fee is False:
        response = 'You have not paid the one-time membership fee, please pay'
        requirement = 'pay_membership_fee'
        return success, response, requirement

    # check if user account is active
    if profile.status != 'active':
        response = f'Your account is {profile.status}, please contact admin'
        requirement = 'activate_account'
        return success, response, requirement

    # Check if user have valid card
    if not UserCard.objects.filter(user=profile).exists():
        response = 'No valid card in your account, please add a card to qualify for loan'
        requirement = 'add_card'
        return success, response, requirement

    # Check if user meets guarantors requirement
    if Guarantor.objects.filter(user=profile, confirmed=True).exclude(guarantor=profile).count() < loan_settings.number_of_guarantor:
        response = f"You must have {loan_settings.number_of_guarantor} guarantor(s) before you can apply for loan"
        requirement = 'add_guarantor'
        return success, response, requirement

    # check if user still have a pending loan
    query = Q(user=profile)
    exclude = Q(status='unapproved') | Q(status='repaid')
    if Loan.objects.filter(query).exclude(exclude).exists():
        response = f"You cannot apply for a loan at the moment because you still have a loan running on your account."
        requirement = 'active_loan'
        return success, response, requirement

    success = True
    response = "Eligible for loan"
    requirement = 'fulfilled'
    return success, response, requirement


def verify_loan_repayment(gateway, reference):
    success = True
    response = None
    transaction_id = loan_id = email = None
    amount = 0

    if gateway == 'paystack':
        success, response = verify_paystack_transaction(reference)

        if success is False:
            return success, response

        # tokenize/save user card
        tokenize_user_card(response)

        email = response['email']
        amount = response['amount']
        transaction_id = response['payload']['data']['metadata']['transaction_id']
        payment_type = response['payload']['data']['metadata']['payment_type']
        loan_id = response['payload']['data']['metadata']['loan_id']

    try:
        trans = LoanTransaction.objects.get(id=transaction_id, user__user__email__iexact=email)
    except Exception as ex:
        return False, str(ex)

    if trans.status == 'success':
        return success, 'This transaction is already processed'

    trans.reference = reference
    trans.status = 'success'
    trans.response = response
    trans.save()

    # update loan data
    try:
        loan = Loan.objects.get(id=loan_id)
    except Exception as ex:
        return False, str(ex)

    loan.amount_repaid += decimal.Decimal(amount)
    loan.last_repayment_date = timezone.now()
    loan.next_repayment_date = loan.start_date + timezone.timedelta(days=get_loan_repayment_count(loan.duration))
    if loan.amount_repaid >= loan.amount_to_repay:
        loan.status = 'repaid'
    loan.save()

    return True, "Loan repayment verified and processed"


def do_loan_repayment(profile, loan_id, amount, **kwargs):
    request = kwargs.get('request')
    callback_url = kwargs.get('callback_url')
    success = True
    response = 'Loan processed successfully'
    card_id = kwargs.get('card_id')
    gateway = None

    if request:
        gateway = request.data.get('payment_gateway')

    if not callback_url:
        callback_url = None
        if request:
            callback_url = f"{request.scheme}://{request.get_host()}{request.path}"

    try:
        loan = Loan.objects.get(user=profile, id=loan_id)
    except Exception as ex:
        return False, f"{ex}"

    amt_to_repay = loan.amount_to_repay
    amt_repaid = loan.amount_repaid
    amt_left_to_repay = loan.get_amount_left_to_repay()

    if amt_repaid >= amt_to_repay:
        return False, f"Loan payment already completed"

    if float(amount) > float(amt_left_to_repay):
        amount = amt_left_to_repay

    transaction, created = LoanTransaction.objects.get_or_create(
        user=profile, loan=loan, transaction_type='repayment', amount=amount, status='pending'
    )

    metadata = {
        'payment_type': 'loan_repayment',
        'loan_id': loan.id,
        'transaction_id': transaction.id,
    }

    # when card is not selected by user
    if not card_id:
        if not gateway:
            return False, "payment gateway is required"

        transaction.payment_method = gateway
        transaction.save()

        success, response = get_paystack_link(
            email=profile.user.email,
            amount=amount,
            metadata=metadata,
            callback_url=callback_url
        )
        return success, response

    # when card is selected by user
    if card_id:
        try:
            card = UserCard.objects.get(user=profile, id=card_id)
        except Exception as ex:
            return False, f"{ex}"

        transaction.payment_method = card.gateway
        transaction.save()

        authorization_code = card.authorization_code
        email = profile.user.email

        success, response = paystack_auto_charge(
            authorization_code=authorization_code, email=email, amount=amount, metadata=metadata
        )
        if success is False:
            return success, response.get('message')

        reference = response['data']['reference']
        success, response = verify_loan_repayment(card.gateway, reference)

    return success, response


