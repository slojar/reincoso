from rest_framework import serializers
from .models import *


class LoanDurationSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoanDuration
        exclude = ['created_on', 'updated_on']

