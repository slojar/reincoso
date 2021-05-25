from rest_framework import serializers
from .models import *


class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        exclude = ['id']


class FeedbackMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackMessage
        exclude = []


class UserDetailSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    cards = serializers.SerializerMethodField()
    guarantors = serializers.SerializerMethodField()

    def get_first_name(self, obj):
        return obj.first_name()

    def get_last_name(self, obj):
        return obj.last_name()

    def get_email(self, obj):
        return obj.email()

    def get_guarantors(self, obj):
        guarantors = [guarantor.guarantor for guarantor in Guarantor.objects.filter(user=obj).distinct()
                      if guarantor.guarantor != obj]
        return UserDetailSerializer(guarantors, many=True).data

    def get_cards(self, obj):
        return UserCard.objects.filter(user=obj).values('id', 'bank', 'card_type', 'bin', 'last4', 'exp_month',
                                                        'exp_year', 'default') or None

    class Meta:
        model = Profile
        exclude = ['bvn', 'user']


class GuarantorSerializer(serializers.ModelSerializer):
    # guarantor = serializers.SerializerMethodField()
    # guarantor = UserDetailSerializer()

    # def get_guarantor(self, obj):
    #     return UserDetailSerializer(obj.guarantor).data

    class Meta:
        model = Guarantor
        exclude = ['id', 'user']

