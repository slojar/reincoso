from django.contrib import admin
from .models import *


@admin.register(InvestmentDuration)
class InvestmentDurationAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'duration', 'number_of_days', 'percentage', 'created_on', 'updated_on']


@admin.register(AvailableInvestment)
class InvestmentDurationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'status', 'created_on', 'updated_on']


@admin.register(InvestmentOption)
class InvestmentDurationAdmin(admin.ModelAdmin):
    list_display = ['id', 'investment', 'name', 'status', 'created_on', 'updated_on']


@admin.register(InvestmentSpecification)
class InvestmentDurationAdmin(admin.ModelAdmin):
    list_display = ['id', 'investment_option', 'key', 'value', 'visible', 'status', 'created_on', 'updated_on']


@admin.register(Investment)
class InvestmentDurationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'investment', 'option', 'duration', 'amount_invested', 'return_on_invested', 'status', 'created_on', 'updated_on']
    raw_id_fields = ['user']
    search_fields = ['user__user__username', 'user__user__email', 'user__user__first_name', 'user__user__last_name', 'user__phone_number']
    list_filter = ['investment', 'option', 'duration', 'status', 'created_on', 'updated_on']

