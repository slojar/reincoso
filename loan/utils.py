import calendar
import decimal
from loan.models import *
from django.utils import timezone
from savings.models import SavingTransaction


def get_loan_offer(profile):
    success = False
    response = ""
    loan_settings, created = LoanSetup.objects.get_or_create(site=Site.objects.get_current())
    last_six_month = timezone.now() - timezone.timedelta(days=loan_settings.eligibility_days)
    savings_transaction = SavingTransaction.objects.filter(user=profile, status='success').last()

    if not savings_transaction:
        response = "Sorry, you are unable to get a loan right now. make sure you have saved for at least " \
                         "6 months before applying for loan."
        return success, response

    eligible = last_six_month >= savings_transaction.created_on

    if not eligible:
        response = "Sorry, you are unable to get a loan right now. make sure you have saved for at least " \
                         "6 months before applying for loan."
        return success, response

    success = True
    response = round(savings_transaction.saving.total * loan_settings.offer, 2)
    return success, response


def create_loan(profile, amount, duration):
    success = True
    response = "Loan application successful, please wait while we process your loan"
    repayment_day_count = 0

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

    loan.next_repayment_date = loan.start_date + timezone.timedelta(days=repayment_day_count)
    loan.status = "processing"
    loan.save()

    return success, response


