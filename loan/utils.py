import calendar
import decimal
from loan.models import *
from django.utils import timezone
from savings.models import SavingTransaction
from settings.models import LoanSetting
from account.models import UserCard, Guarantor
from django.db.models import Q


def get_loan_offer(profile):
    success = False
    response = ""
    loan_settings, created = LoanSetting.objects.get_or_create(site=Site.objects.get_current())
    savings_transaction = SavingTransaction.objects.filter(user=profile, status='success').last()

    if not savings_transaction:
        response = "Sorry, you are unable to get a loan right now. make sure you have saved for at least " \
                         "6 months before applying for loan."
        return success, response

    last_six_month = timezone.now() - timezone.timedelta(days=loan_settings.eligibility_days)
    eligible = last_six_month >= savings_transaction.created_on

    if not eligible:
        response = "Sorry, you are unable to get a loan right now. make sure you have saved for at least " \
                         "6 months before applying for loan."
        return success, response

    success = True
    response = round(savings_transaction.saving.total * loan_settings.offer, 2)
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


def create_loan(profile, amount, duration):
    success = True
    response = "Loan application successful, please wait while we process your loan"

    amount = decimal.Decimal(amount)
    loan = Loan.objects.create(user=profile)
    loan.amount = amount

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



