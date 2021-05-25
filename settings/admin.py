from django.contrib import admin
from .models import *


class LoanSetupAdmin(admin.ModelAdmin):
    list_display = ['id', 'site']


class PaymentGatewayInline(admin.TabularInline):
    model = PaymentGateway
    extra = 0


class SettingsAdmin(admin.ModelAdmin):
    list_display = ['id', 'site_name']
    list_display_links = ['id', 'site_name']
    inlines = [PaymentGatewayInline]


admin.site.register(GeneralSettings, SettingsAdmin)
admin.site.register(LoanSetting, LoanSetupAdmin)


