from django.contrib.admin.models import LogEntry
from rest_framework import serializers
from account.models import Withdrawal
from superadmin.models import AdminNotification, InvestmentWithdrawal


class ActivityReportSerializer(serializers.ModelSerializer):
    action_flag = serializers.SerializerMethodField()
    user = serializers.CharField(source='user.email')
    content_type = serializers.CharField(source='content_type.model')
    change_message = serializers.SerializerMethodField()

    def get_change_message(self, obj):
        if obj.get_action_flag_display() == 'Addition':
            message = f'added: {obj.content_type.model} - ID:{obj.object_id}'
            return message
        elif obj.get_action_flag_display() == 'Change':
            message = str(obj.change_message)
            message = message.replace('"', "").replace("[", "").replace("{", "").replace("]", "")
            message = message.replace("}", "").replace("fields:", "") + f' on {obj.content_type.model} - ID:{obj.object_id}'
            if "logged".capitalize() in message:
                message = "Logged in"
            return message
        elif obj.get_action_flag_display() == 'Deletion':
            message = f'deleted: {obj.content_type.model} - ID:{obj.object_id}'
            return message
        else:
            return None

    def get_action_flag(self, obj):
        return obj.get_action_flag_display()

    class Meta:
        model = LogEntry
        exclude = ['object_id', 'object_repr']


class WithdrawalSerializer(serializers.ModelSerializer):
    requested_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    def get_requested_by(self, obj):
        data = {
            "first_name": obj.requested_by.first_name,
            "last_name": obj.requested_by.last_name,
            "email": obj.requested_by.email,
            "username": obj.requested_by.username,
        }
        return data

    def get_updated_by(self, obj):
        data = {
            "username": obj.requested_by.username,
            "email": obj.requested_by.email,
        }
        return data

    class Meta:
        model = Withdrawal
        exclude = []


class AdminNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminNotification
        exclude = []


class InvestmentWithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentWithdrawal
        exclude = []

