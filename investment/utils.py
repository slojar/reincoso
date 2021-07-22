from .models import *


def create_investment(request):
    success = True
    response = "Investment created successfully"
    user = request.user.profile
    investment = request.data.get('investment_id')
    option = request.data.get('option_id')
    duration = request.data.get('duration_id')
    amount = request.data.get('amount')

    try:
        investment = AvailableInvestment.objects.get(id=investment)
        option = InvestmentOption.objects.get(id=option)
        duration = InvestmentDuration.objects.get(id=duration)
    except Exception as ex:
        return False, str(ex)

    investment, created = Investment.objects.get_or_create(
        user=user, investment=investment, option=option, duration=duration, amount_invested=amount
    )
    calc_roi = (amount * duration.percentage) / 100
    investment.return_on_invested = amount + calc_roi
    investment.number_of_month = duration.duration
    investment.number_of_days = duration.number_of_days
    investment.percentage = duration.percentage
    investment.save()

    return success, investment




