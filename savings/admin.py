from django.contrib import admin
from .models import *


class SavingTransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'saving', 'amount', 'status', 'reference', 'created_on', 'updated_on']
    list_filter = ['status', 'payment_method']
    search_fields = ['reference']


class SavingTransactionInline(admin.TabularInline):
    model = SavingTransaction
    extra = 0


class SavingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount']
    inlines = [SavingTransactionInline]


admin.site.register(Duration)
admin.site.register(Saving, SavingAdmin)
admin.site.register(SavingTransaction, SavingTransactionAdmin)
