from django.contrib import admin
from .models import *


class SavingsTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'active', 'created_on', 'updated_on']
    list_filter = ['active', 'created_on', 'updated_on']


class SavingTransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'saving', 'amount', 'status', 'reference', 'created_on', 'updated_on']
    list_filter = ['status', 'payment_gateway']
    search_fields = ['reference']
    ordering = ['-id']


class SavingTransactionInline(admin.TabularInline):
    model = SavingTransaction
    extra = 0
    raw_id_fields = ['user']


class SavingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'type', 'auto_save', 'amount', 'last_payment', 'total', 'status', 'created_on', 'updated_on']
    list_filter = ['auto_save', 'type', 'duration', 'last_payment_date', 'payment_gateway', 'status', 'created_on', 'updated_on']
    search_fields = [
        'savingtransaction__reference', 'user__user__first_name', 'user__user__last_name', 'user__user__email'
    ]
    raw_id_fields = ['user']
    inlines = [SavingTransactionInline]


admin.site.register(SavingsType, SavingsTypeAdmin)
admin.site.register(Saving, SavingAdmin)
admin.site.register(SavingTransaction, SavingTransactionAdmin)
admin.site.register(Duration)
