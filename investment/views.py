from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics

from loan.paginations import CustomPagination
from .models import *
from .serializers import *
from .utils import *


class InvestmentsView(generics.ListAPIView):
    queryset = AvailableInvestment.objects.all()
    serializer_class = AvailableInvestmentSerializer


class InvestmentDetailView(generics.RetrieveAPIView):
    queryset = AvailableInvestment.objects.all()
    serializer_class = AvailableInvestmentSerializer

    def retrieve(self, request, *args, **kwargs):
        data = dict()
        id_ = self.kwargs.get('id')
        try:
            avail_investment = AvailableInvestment.objects.get(id=id_)
        except Exception as ex:
            try:
                avail_investment = AvailableInvestment.objects.get(name__iexact=id_)
            except Exception as ex:
                data['detail'] = str(ex)
                return Response(data, status.HTTP_404_NOT_FOUND)
        data = AvailableInvestmentSerializer(avail_investment).data
        return Response(data)


class MyInvestmentView(generics.ListAPIView):
    serializer_class = InvestmentSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return Investment.objects.filter(user=self.request.user.profile)


class MyInvestmentDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = InvestmentSerializer
    queryset = Investment.objects.all()
    lookup_field = 'id'


class InvestView(APIView):

    def post(self, request):
        data = dict()
        success, response = create_investment(profile=request.user.profile, data=request.data)
        if success is False:
            data['detail'] = response
            return Response(data, status.HTTP_400_BAD_REQUEST)

        data['detail'] = "Investment created successfully"
        data['data'] = InvestmentSerializer(response).data
        return Response(data)


class InvestPaymentView(APIView):

    def post(self, request):
        data = dict()
        investment_id = request.data.get('investment_id')
        card_id = request.data.get('card_id')
        user = request.user.profile

        success, response = investment_payment(request.user.profile, request.data)

        if success is False:
            data['detail'] = "There is an error with request sent"
            data['data'] = response
            return Response(data, status.HTTP_400_BAD_REQUEST)

        data['detail'] = response
        if card_id:
            data['data'] = InvestmentSerializer(Investment.objects.get(id=investment_id, user=user)).data
        return Response(data)



