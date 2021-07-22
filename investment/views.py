from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from .models import *
from .serializers import *
from .utils import *


class InvestmentsView(generics.ListAPIView):
    queryset = AvailableInvestment.objects.all()
    serializer_class = AvailableInvestmentSerializer


class InvestView(APIView):

    def post(self, request):
        data = dict()
        success, response = create_investment(request)
        if success is False:
            data['detail'] = response
            return Response(data, status.HTTP_400_BAD_REQUEST)

        data['detail'] = "Investment created successfully"
        data['data'] = InvestmentSerializer(response).data
        return Response(data)

