from django.contrib.admin.models import LogEntry
from rest_framework import serializers


class ActivityReportSerializer(serializers.ModelSerializer):
    action_flag = serializers.SerializerMethodField()
    user = serializers.CharField(source='user.email')
    content_type = serializers.CharField(source='content_type.model')

    def get_action_flag(self, obj):
        return obj.get_action_flag_display()

    class Meta:
        model = LogEntry
        exclude = ['object_id', 'object_repr']
#
