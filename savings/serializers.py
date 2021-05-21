from rest_framework import serializers
from savings.models import *


class SavingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saving
        exclude = []


class SavingDurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Duration
        exclude = []

