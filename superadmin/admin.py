from django.contrib import admin
from .models import AdminNotification, InvestmentWithdrawal


class InvestmentWithdrawalAdmin(admin.ModelAdmin):
    list_display = ['investment', 'status', 'amount_requested']


admin.site.register(AdminNotification)
admin.site.register(InvestmentWithdrawal, InvestmentWithdrawalAdmin)

