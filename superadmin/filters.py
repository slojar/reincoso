from django_filters import rest_framework as filters
from account.models import *
from loan.models import *
from savings.models import *
from investment.models import *
from settings.models import *


class WalletFilter(filters.FilterSet):
    first_name = filters.CharFilter(field_name='user__user__first_name', lookup_expr='icontains')
    last_name = filters.CharFilter(field_name='user__user__last_name', lookup_expr='icontains')
    phone_number = filters.CharFilter(field_name='user__phone_number', lookup_expr='icontains')
    member_id = filters.CharFilter(field_name='user__member_id', lookup_expr='iexact')
    min_balance = filters.NumberFilter(field_name='balance', lookup_expr='gte')
    max_balance = filters.NumberFilter(field_name='balance', lookup_expr='lte')
    min_bonus = filters.NumberFilter(field_name='bonus', lookup_expr='gte')
    max_bonus = filters.NumberFilter(field_name='bonus', lookup_expr='lte')
    date_from = filters.DateTimeFilter(field_name='created_on', lookup_expr='gte')
    date_to = filters.DateTimeFilter(field_name='created_on', lookup_expr='lte')

    class Meta:
        model = Wallet
        exclude = []


class LoanFilter(filters.FilterSet):
    first_name = filters.CharFilter(field_name='user__user__first_name', lookup_expr='icontains')
    last_name = filters.CharFilter(field_name='user__user__last_name', lookup_expr='icontains')
    phone_number = filters.CharFilter(field_name='user__phone_number', lookup_expr='icontains')
    member_id = filters.CharFilter(field_name='user__member_id', lookup_expr='iexact')
    min_amount = filters.NumberFilter(field_name='amount', lookup_expr='gte')
    max_amount = filters.NumberFilter(field_name='amount', lookup_expr='lte')
    duration = filters.CharFilter(field_name='duration__title', lookup_expr='iexact')
    basis = filters.CharFilter(field_name='basis', lookup_expr='iexact')
    min_number_of_days = filters.NumberFilter(field_name='number_of_days', lookup_expr='gte')
    max_number_of_days = filters.NumberFilter(field_name='number_of_days', lookup_expr='lte')
    min_percentage = filters.NumberFilter(field_name='percentage', lookup_expr='gte')
    max_percentage = filters.NumberFilter(field_name='percentage', lookup_expr='lte')
    min_start_date = filters.NumberFilter(field_name='start_date', lookup_expr='gte')
    max_start_date = filters.NumberFilter(field_name='start_date', lookup_expr='lte')
    min_next_repayment_date = filters.NumberFilter(field_name='next_repayment_date', lookup_expr='gte')
    max_next_repayment_date = filters.NumberFilter(field_name='next_repayment_date', lookup_expr='lte')
    status = filters.CharFilter(field_name='status', lookup_expr='iexact')
    date_from = filters.DateTimeFilter(field_name='created_on', lookup_expr='gte')
    date_to = filters.DateTimeFilter(field_name='created_on', lookup_expr='lte')

    class Meta:
        model = Loan
        exclude = []


class InvestmentFilter(filters.FilterSet):
    first_name = filters.CharFilter(field_name='user__user__first_name', lookup_expr='icontains')
    last_name = filters.CharFilter(field_name='user__user__last_name', lookup_expr='icontains')
    phone_number = filters.CharFilter(field_name='user__phone_number', lookup_expr='icontains')
    member_id = filters.CharFilter(field_name='user__member_id', lookup_expr='iexact')
    min_percentage = filters.NumberFilter(field_name='percentage', lookup_expr='gte')
    max_percentage = filters.NumberFilter(field_name='percentage', lookup_expr='lte')
    min_start_date = filters.NumberFilter(field_name='start_date', lookup_expr='gte')
    max_start_date = filters.NumberFilter(field_name='start_date', lookup_expr='lte')
    min_number_of_month = filters.NumberFilter(field_name='number_of_month', lookup_expr='gte')
    max_number_of_month = filters.NumberFilter(field_name='number_of_month', lookup_expr='lte')
    min_number_of_days = filters.NumberFilter(field_name='number_of_days', lookup_expr='gte')
    max_number_of_days = filters.NumberFilter(field_name='number_of_days', lookup_expr='lte')
    min_amount_invested = filters.NumberFilter(field_name='amount_invested', lookup_expr='gte')
    max_amount_invested = filters.NumberFilter(field_name='amount_invested', lookup_expr='lte')
    min_return_on_invested = filters.NumberFilter(field_name='return_on_invested', lookup_expr='gte')
    max_return_on_invested = filters.NumberFilter(field_name='return_on_invested', lookup_expr='lte')
    status = filters.CharFilter(field_name='status', lookup_expr='iexact')
    date_from = filters.DateTimeFilter(field_name='created_on', lookup_expr='gte')
    date_to = filters.DateTimeFilter(field_name='created_on', lookup_expr='lte')

    class Meta:
        model = Investment
        exclude = []


class SavingFilter(filters.FilterSet):
    first_name = filters.CharFilter(field_name='user__user__first_name', lookup_expr='icontains')
    last_name = filters.CharFilter(field_name='user__user__last_name', lookup_expr='icontains')
    phone_number = filters.CharFilter(field_name='user__phone_number', lookup_expr='icontains')
    member_id = filters.CharFilter(field_name='user__member_id', lookup_expr='iexact')
    min_total = filters.NumberFilter(field_name='total', lookup_expr='gte')
    max_total = filters.NumberFilter(field_name='total', lookup_expr='lte')
    # status = filters.CharFilter(field_name='status', lookup_expr='iexact')
    date_from = filters.DateTimeFilter(field_name='created_on', lookup_expr='gte')
    date_to = filters.DateTimeFilter(field_name='created_on', lookup_expr='lte')

    class Meta:
        model = Saving
        exclude = []


