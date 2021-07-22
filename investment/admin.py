from django.contrib import admin
from .models import *


# INLINES
class InvestmentSpecInline(admin.TabularInline):
    model = InvestmentSpecification
    extra = 1


class InvestmentOptionInline(admin.TabularInline):
    model = InvestmentOption
    extra = 1


@admin.register(InvestmentDuration)
class InvestmentDurationAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'duration', 'number_of_days', 'percentage', 'created_on', 'updated_on']


@admin.register(AvailableInvestment)
class AvailableInvestmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'status', 'created_on', 'updated_on']
    inlines = [
        InvestmentOptionInline
    ]


@admin.register(InvestmentOption)
class InvestmentOptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'available_investment', 'name', 'status', 'created_on', 'updated_on']
    inlines = [InvestmentSpecInline]


@admin.register(InvestmentSpecification)
class InvestmentSpecificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'investment_option', 'key', 'value', 'visible', 'status', 'created_on', 'updated_on']


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'investment', 'option', 'duration', 'amount_invested', 'return_on_invested', 'status', 'created_on', 'updated_on']
    raw_id_fields = ['user']
    search_fields = ['user__user__username', 'user__user__email', 'user__user__first_name', 'user__user__last_name', 'user__phone_number']
    list_filter = ['investment', 'option', 'duration', 'status', 'created_on', 'updated_on']

