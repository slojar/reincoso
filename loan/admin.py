from django.contrib import admin
from .models import *


class LoanDurationAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'basis', 'duration', 'number_of_days', 'percentage', 'created_on', 'updated_on']
    list_filter = ['created_on', 'updated_on']


class LoanTransactionInline(admin.TabularInline):
    model = LoanTransaction
    extra = 0
    ordering = ['-id']


class LoanAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'number_of_days', 'status', 'created_on', 'updated_on']
    list_filter = ['status', 'duration', 'start_date', 'end_date', 'last_repayment_date', 'next_repayment_date',
                   'created_on', 'updated_on']
    inlines = [LoanTransactionInline]


class LoanTransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'transaction_type', 'amount', 'status', 'payment_method', 'created_on', 'updated_on']
    list_display_links = ['id', 'user']


admin.site.register(LoanTransaction, LoanTransactionAdmin)
admin.site.register(LoanDuration, LoanDurationAdmin)
admin.site.register(Loan, LoanAdmin)

