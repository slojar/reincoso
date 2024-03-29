from rest_framework import serializers
from superadmin.models import InvestmentWithdrawal

from .models import *


class InvestmentDurationSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvestmentDuration
        exclude = []


class InvestmentOptionSerializer(serializers.ModelSerializer):

    specification = serializers.SerializerMethodField()
    # duration = InvestmentDurationSerializer()

    def get_specification(self, obj):
        query = InvestmentSpecification.objects.filter(option=obj, visible=True, status='active')
        return InvestmentSpecificationSerializer(query, many=True).data

    class Meta:
        model = InvestmentOption
        exclude = []
        depth = 2


class InvestmentSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    def get_options(self, obj):
        if InvestmentOption.objects.filter(investment=obj).exists():
            query = InvestmentOption.objects.filter(investment=obj)
            return InvestmentOptionSerializer(query, many=True).data
        return None

    class Meta:
        model = Investment
        exclude = []
        depth = 1


class InvestmentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvestmentType
        exclude = []


class InvestmentSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentSpecification
        exclude = []


class UserInvestmentSerializer(serializers.ModelSerializer):
    investment = serializers.CharField(source='investment.name', read_only=True)
    option = serializers.CharField(source='option.name', read_only=True)
    duration = serializers.CharField(source='duration.title', read_only=True)
    current_balance = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    withdrawals = serializers.SerializerMethodField()

    def get_current_balance(self, obj):
        return obj.amount_invested + obj.amount_yield

    def get_user(self, obj):
        user = {
            'first_name': obj.user.user.first_name,
            'last_name': obj.user.user.last_name,
            'email': obj.user.user.email,
            'phone_number': obj.user.phone_number,
        }
        return user

    def get_withdrawals(self, obj):
        if InvestmentWithdrawal.objects.filter(investment=obj).exists():
            queryset = InvestmentWithdrawal.objects.filter(investment=obj)
            data = [{
                'id': instance.id,
                'amount_requested': instance.amount_requested,
                'narration': instance.narration,
                'status': instance.status,
                'created_on': instance.created_on,
                'updated_on': instance.updated_on
            } for instance in queryset]
            return data
        return None
        # from account.serializers import UserDetailSerializer
        # return UserDetailSerializer(obj.user).data

    class Meta:
        depth = 1
        model = UserInvestment
        exclude = []




