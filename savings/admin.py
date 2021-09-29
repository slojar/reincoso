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


class SavingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'type', 'amount', 'status', 'auto_save']
    list_filter = ['type', 'last_payment_date', 'status']
    inlines = [SavingTransactionInline]


admin.site.register(SavingsType, SavingsTypeAdmin)
admin.site.register(Saving, SavingAdmin)
admin.site.register(SavingTransaction, SavingTransactionAdmin)
admin.site.register(Duration)
