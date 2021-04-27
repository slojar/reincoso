from rest_framework import serializers
from savings.models import *


class SavingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saving
        exclude = []

