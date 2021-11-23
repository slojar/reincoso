from django_filters import rest_framework as filters
from account.models import *
from loan.models import *
from savings.models import *
from investment.models import *
from settings.models import *


class WalletFilter(filters.FilterSet):
    email = filters.CharFilter(field_name='user__user__email', lookup_expr='iexact')
    min_balance = filters.NumberFilter(field_name='balance', lookup_expr='gte')
    max_balance = filters.NumberFilter(field_name='balance', lookup_expr='lte')
    min_bonus = filters.NumberFilter(field_name='bonus', lookup_expr='gte')
    max_bonus = filters.NumberFilter(field_name='bonus', lookup_expr='lte')
    date_from = filters.DateTimeFilter(field_name='created_on', lookup_expr='gte')
    date_to = filters.DateTimeFilter(field_name='created_on', lookup_expr='lte')

    class Meta:
        model = Wallet
        fields = ['email', 'min_balance', 'max_balance', 'min_bonus', 'max_bonus', 'date_from', 'date_to']


class LoanFilter(filters.FilterSet):
    email = filters.CharFilter(field_name='user__user__email', lookup_expr='iexact')
    min_amount = filters.NumberFilter(field_name='amount', lookup_expr='gte')
    max_amount = filters.NumberFilter(field_name='amount', lookup_expr='lte')
    duration = filters.CharFilter(field_name='duration__title', lookup_expr='iexact')
    basis = filters.CharFilter(field_name='basis', lookup_expr='iexact')
    min_number_of_days = filters.NumberFilter(field_name='number_of_days', lookup_expr='gte')
    max_number_of_days = filters.NumberFilter(field_name='number_of_days', lookup_expr='lte')
    min_percentage = filters.NumberFilter(field_name='percentage', lookup_expr='gte')
    max_percentage = filters.NumberFilter(field_name='percentage', lookup_expr='lte')
    min_start_date = filters.DateTimeFilter(field_name='start_date', lookup_expr='gte')
    max_start_date = filters.DateTimeFilter(field_name='start_date', lookup_expr='lte')
    min_next_repayment_date = filters.DateTimeFilter(field_name='next_repayment_date', lookup_expr='gte')
    max_next_repayment_date = filters.DateTimeFilter(field_name='next_repayment_date', lookup_expr='lte')
    status = filters.CharFilter(field_name='status', lookup_expr='iexact')
    date_from = filters.DateTimeFilter(field_name='created_on', lookup_expr='gte')
    date_to = filters.DateTimeFilter(field_name='created_on', lookup_expr='lte')

    class Meta:
        model = Loan
        fields = [
            'email', 'min_amount', 'max_amount', 'duration', 'basis', 'min_number_of_days', 'max_number_of_days',
            'min_percentage', 'max_percentage', 'min_start_date', 'max_start_date', 'min_next_repayment_date',
            'max_next_repayment_date', 'status', 'date_from', 'date_to'
        ]


class InvestmentFilter(filters.FilterSet):
    investment_type = filters.CharFilter(field_name='type__name', lookup_expr='iexact')
    active = filters.BooleanFilter(field_name='active')
    date_from = filters.DateTimeFilter(field_name='created_on', lookup_expr='gte')
    date_to = filters.DateTimeFilter(field_name='created_on', lookup_expr='lte')

    class Meta:
        model = Investment
        fields = ['investment_type', 'active', 'date_from', 'date_to']


class SavingFilter(filters.FilterSet):
    email = filters.CharFilter(field_name='user__user__email', lookup_expr='iexact')
    saving_type = filters.CharFilter(field_name='type__name', lookup_expr='iexact')
    duration = filters.CharFilter(field_name='duration__name', lookup_expr='iexact')
    min_total = filters.NumberFilter(field_name='total', lookup_expr='gte')
    max_total = filters.NumberFilter(field_name='total', lookup_expr='lte')
    auto_save = filters.BooleanFilter(field_name='auto_save')
    # status = filters.CharFilter(field_name='status', lookup_expr='iexact')
    date_from = filters.DateTimeFilter(field_name='created_on', lookup_expr='gte')
    date_to = filters.DateTimeFilter(field_name='created_on', lookup_expr='lte')

    class Meta:
        model = Saving
        fields = ['email', 'saving_type', 'duration', 'min_total', 'max_total', 'auto_save', 'date_from', 'date_to']


class ProfileFilter(filters.FilterSet):
    email = filters.CharFilter(field_name='user__email', lookup_expr='iexact')
    gender = filters.CharFilter(field_name='gender', lookup_expr='iexact')
    status = filters.CharFilter(field_name='status', lookup_expr='iexact')
    paid_membership = filters.BooleanFilter(field_name='paid_membership_fee')
    date_from = filters.DateTimeFilter(field_name='created_on', lookup_expr='gte')
    date_to = filters.DateTimeFilter(field_name='created_on', lookup_expr='lte')

    class Meta:
        model = Profile
        fields = ['email', 'gender', 'status', 'paid_membership', 'date_from', 'date_to']

