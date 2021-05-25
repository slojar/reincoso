from django.contrib import admin
from .models import *


class UserCardInline(admin.StackedInline):
    model = UserCard
    extra = 0
    fk_name = 'user'


class GuarantorInline(admin.TabularInline):
    model = Guarantor
    extra = 0
    fk_name = 'user'


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'phone_number', 'gender', 'status', 'paid_membership_fee', 'created_on', 'updated_on']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    list_filter = ['paid_membership_fee', 'gender', 'status', 'created_on', 'updated_on']
    inlines = [
        GuarantorInline,
        UserCardInline,
    ]


admin.site.register(Profile, ProfileAdmin)
admin.site.register(FaqCategory)
admin.site.register(Faq)
admin.site.register(FeedbackMessage)
