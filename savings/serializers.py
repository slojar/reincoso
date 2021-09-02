from rest_framework import serializers
from savings.models import *


class SavingsTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingTransaction
        exclude = ['response', 'user', 'saving']


class SavingSerializer(serializers.ModelSerializer):
    transactions = serializers.SerializerMethodField()
    successful_transaction = serializers.SerializerMethodField()

    def get_successful_transaction(self, obj):
        return SavingTransaction.objects.filter(saving=obj, status='success').count()

    def get_transactions(self, obj):
        trans = SavingTransaction.objects.filter(saving=obj)[:10]
        return SavingsTransactionSerializer(trans, many=True).data

    class Meta:
        model = Saving
        exclude = ['user']
        depth = 2


class SavingDurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Duration
        exclude = []

