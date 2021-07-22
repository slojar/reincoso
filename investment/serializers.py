from rest_framework import serializers
from .models import *


class InvestmentDurationSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvestmentDuration
        exclude = []


class InvestmentOptionSerializer(serializers.ModelSerializer):

    specification = serializers.SerializerMethodField()
    duration = InvestmentDurationSerializer()

    def get_specification(self, obj):
        query = InvestmentSpecification.objects.filter(investment_option=obj, visible=True, status='active')
        return InvestmentSpecificationSerializer(query, many=True).data

    class Meta:
        model = InvestmentOption
        exclude = ['status']


class AvailableInvestmentSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    def get_options(self, obj):
        query = InvestmentOption.objects.filter(available_investment=obj, status='active')
        return InvestmentOptionSerializer(query, many=True).data

    class Meta:
        model = AvailableInvestment
        exclude = []


class InvestmentSpecificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvestmentSpecification
        exclude = ['visible']


class InvestmentSerializer(serializers.ModelSerializer):
    investment = serializers.CharField(source='investment.name')
    option = serializers.CharField(source='option.name')
    duration = serializers.CharField(source='duration.title')

    class Meta:
        model = Investment
        exclude = []




