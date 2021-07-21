from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from .models import *
from .serializers import *


class InvestmentsView(generics.ListAPIView):
    queryset = ''



