from ast import arg
from threading import Thread

from django.db.models import Sum

from account.models import Profile
from superadmin.models import InvestmentWithdrawal
from .models import Investment, UserInvestment
from django.utils import timezone
from account.send_email import send_email_using_mailgun
from django.conf import settings

naira_unicode = settings.NAIRA_UNICODE


def investment_maturity_check() -> None:
    matured = UserInvestment.objects.filter(status="approved", end_date__date=timezone.now().date())
    subject: str = "Investment with Reincoso"

    if matured is not None:
        for investment in matured:
            body: str = f"""
    Dear {investment.user.user.first_name},
    
    We are pleased to notify you that your {naira_unicode}{investment.amount_invested} investment in {investment.investment.name} has matured and interest will be paid to you shortly.
    For any further inquiry please contact us on:
    Email - coopadmin@reincoso.com
    """
            send_email_using_mailgun(recipient=investment.user.user.email, subject=subject, message=body)


def update_investment_yield():
    investments = UserInvestment.objects.filter(status="approved", end_date__lte=timezone.datetime.now())

    for investment in investments:
        withdrawal = InvestmentWithdrawal.objects.filter(investment=investment, status="disbursed")
        withdrawn_amount = withdrawal.aggregate(Sum('amount_requested'))['amount_requested__sum'] or 0
        roi = investment.return_on_invested
        amount_invested = investment.amount_invested

        profit = roi - amount_invested
        if withdrawn_amount > 0:
            profit = (roi - amount_invested) - withdrawn_amount
        profit_split = profit / 12
        investment.amount_yield += profit_split
        investment.save()

    return True


