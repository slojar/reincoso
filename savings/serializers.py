from rest_framework import serializers
from savings.models import *


class SavingsTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingTransaction
        exclude = ['response', 'user', 'saving']


class SavingSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    transactions = serializers.SerializerMethodField()
    successful_transaction = serializers.SerializerMethodField()
    # next_payment_date = serializers.SerializerMethodField()

    def get_user(self, obj):
        user = dict()
        user['first_name'] = obj.user.user.first_name
        user['last_name'] = obj.user.user.last_name
        user['email'] = obj.user.user.email
        user['phone_number'] = obj.user.phone_number
        return user

    def get_successful_transaction(self, obj):
        return SavingTransaction.objects.filter(saving=obj, status='success').count()

    def get_transactions(self, obj):
        trans = SavingTransaction.objects.filter(saving=obj)[:10]
        return SavingsTransactionSerializer(trans, many=True).data

    # def get_next_payment_date(self, obj):
    #     if obj.auto_save is False:
    #         return obj.next_payment_date
    #     return None

    class Meta:
        model = Saving
        exclude = []
        depth = 2


class SavingDurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Duration
        exclude = []


class SavingTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingTransaction
        exclude = []


class SavingsTypeSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    class Meta:
        model = SavingsType
        exclude = []
