from django.contrib import admin
from django.contrib.admin.models import LogEntry

from .models import *


class UserCardInline(admin.StackedInline):
    model = UserCard
    extra = 0
    fk_name = 'user'


class GuarantorInline(admin.TabularInline):
    model = Guarantor
    extra = 0
    fk_name = 'user'


class WalletInline(admin.TabularInline):
    model = Wallet
    extra = 0
    can_delete = False


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'phone_number', 'gender', 'status', 'paid_membership_fee', 'created_on', 'updated_on']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    list_filter = ['paid_membership_fee', 'gender', 'status', 'created_on', 'updated_on']
    inlines = [
        WalletInline,
        GuarantorInline,
        UserCardInline,
    ]


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'

    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'action_flag',
    ]


admin.site.register(Profile, ProfileAdmin)
admin.site.register(FaqCategory)
admin.site.register(Faq)
admin.site.register(Bank)
admin.site.register(FeedbackMessage)
admin.site.register(Withdrawal)
admin.site.register(Guarantor)


