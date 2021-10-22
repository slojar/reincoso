from rest_framework import serializers
from .models import *


class LoanDurationSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoanDuration
        exclude = ['created_on', 'updated_on']


class LoanTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoanTransaction
        exclude = ['loan', 'user', 'response']


class LoanSerializer(serializers.ModelSerializer):
    duration = LoanDurationSerializer(read_only=True)
    transactions = serializers.SerializerMethodField()
    amount_left_to_repay = serializers.DecimalField(source='get_amount_left_to_repay', max_digits=20, decimal_places=2,
                                                    read_only=True)

    def get_transactions(self, obj):
        return LoanTransactionSerializer(LoanTransaction.objects.filter(loan=obj), many=True).data

    class Meta:
        model = Loan
        exclude = ['user']


