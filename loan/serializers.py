from rest_framework import serializers
from .models import *


class LoanDurationSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoanDuration
        exclude = ['created_on', 'updated_on']


class LoanTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoanTransaction
        exclude = ['loan', 'user']


class LoanSerializer(serializers.ModelSerializer):
    duration = LoanDurationSerializer()
    transactions = serializers.SerializerMethodField()
    amount_left_to_repay = serializers.SerializerMethodField()

    def get_amount_left_to_repay(self, obj):
        amt_to_repay = obj.amount_to_repay
        amt_repaid = obj.amount_repaid
        return amt_to_repay - amt_repaid

    def get_transactions(self, obj):
        return LoanTransactionSerializer(LoanTransaction.objects.filter(loan=obj), many=True).data

    class Meta:
        model = Loan
        exclude = ['user']


