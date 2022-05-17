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
    user = serializers.SerializerMethodField()
    duration = LoanDurationSerializer(read_only=True)
    transactions = serializers.SerializerMethodField()
    amount_left_to_repay = serializers.DecimalField(source='get_amount_left_to_repay', max_digits=20, decimal_places=2,
                                                    read_only=True)
    repaid = serializers.SerializerMethodField()

    def get_user(self, obj):
        user = dict()
        user['first_name'] = obj.user.user.first_name
        user['last_name'] = obj.user.user.last_name
        user['email'] = obj.user.user.email
        user['phone_number'] = obj.user.phone_number
        return user

    def get_transactions(self, obj):
        return LoanTransactionSerializer(LoanTransaction.objects.filter(loan=obj), many=True).data

    def get_repaid(self, obj):
        if obj.status == 'repaid':
            return True
        return False

    class Meta:
        model = Loan
        exclude = []


