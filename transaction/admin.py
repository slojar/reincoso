from django.contrib import admin
from .models import *


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'reference', 'status', 'created_on', 'updated_on']
    list_display_links = ['id', 'user']
    list_filter = ['status', 'created_on', 'updated_on']


admin.site.register(Transaction, TransactionAdmin)

