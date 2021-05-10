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


