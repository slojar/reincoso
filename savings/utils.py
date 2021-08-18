from django.db.models import Sum

from savings.models import SavingTransaction


def get_savings_analysis(profile):
    data = dict()
    total_savings = SavingTransaction.objects.filter(user=profile, status='success')
    total_savings = total_savings.aggregate(Sum('amount'))['amount__sum']
    data['total_savings_amount'] = total_savings
    return data

