from .models import *
from rest_framework import serializers


class GeneralSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralSettings
        exclude = []
        

class PaymentGatewaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentGateway
        exclude = []
        
        
class LoanSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanSetting
        exclude = []


