from ast import arg
import logging
from threading import Thread

from django.db.models import Q
from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from account.send_email import failed_investment_mail, successful_investment_mail

from loan.paginations import CustomPagination
from .models import *
from .serializers import *
from .utils import *


class InvestmentsView(generics.ListAPIView):
    queryset = Investment.objects.all()
    serializer_class = InvestmentSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        q = Q(active=True)
        params = self.request.GET
        if params.get('type_id'):
            q = q & Q(type__id=params.get('type_id'))
        if params.get('slug'):
            q = q & Q(type__slug__iexact=params.get('slug'))
        return Investment.objects.filter(q)


class InvestmentDetailView(generics.RetrieveAPIView):
    queryset = Investment.objects.all()
    serializer_class = InvestmentSerializer

    def retrieve(self, request, *args, **kwargs):
        data = dict()
        id_ = self.kwargs.get('id')
        try:
            avail_investment = Investment.objects.get(id=id_)
        except Exception as ex:
            try:
                avail_investment = Investment.objects.get(name__iexact=id_)
            except Exception as ex:
                data['detail'] = str(ex)
                return Response(data, status.HTTP_404_NOT_FOUND)
        data = InvestmentSerializer(avail_investment).data
        return Response(data)


class InvestmentOptionsView(generics.ListAPIView):
    serializer_class = InvestmentOptionSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.kwargs.get('id'):
            return InvestmentOption.objects.filter(investment__id=self.kwargs.get('id'))
        return InvestmentOption.objects.all()


class InvestmentOptionDetailView(generics.RetrieveAPIView):
    lookup_field = 'id'
    queryset = InvestmentOption.objects.all()
    serializer_class = InvestmentOptionSerializer


class MyInvestmentView(generics.ListAPIView):
    serializer_class = UserInvestmentSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return UserInvestment.objects.filter(user=self.request.user.profile)


class MyInvestmentDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserInvestmentSerializer
    queryset = UserInvestment.objects.all()
    lookup_field = 'id'


class InvestmentTypesView(generics.ListAPIView):
    serializer_class = InvestmentTypeSerializer
    pagination_class = CustomPagination
    queryset = InvestmentType.objects.all()


class InvestmentTypesDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = InvestmentTypeSerializer
    lookup_field = 'id'

    def get(self, request, **kwargs):
        id_ = self.kwargs.get('id')
        try:
            query = InvestmentType.objects.get(id=id_)
        except (InvestmentType.DoesNotExist, ValueError):
            query = get_object_or_404(InvestmentType, slug__iexact=id_)
        data = self.serializer_class(query).data

        paginator = CustomPagination()
        investment = Investment.objects.filter(type=query)
        paginated_query = paginator.paginate_queryset(investment, request)
        serialize = InvestmentSerializer(paginated_query, many=True).data
        result = paginator.get_paginated_response(serialize).data
        data['investments'] = result

        return Response(data)


class InvestView(APIView):

    def post(self, request):
        data = dict()
        success, response = create_investment(profile=request.user.profile, data=request.data)

        '''
            INFO: total_amount_invested(): is the total amount invested, can be used to update the amount_invested
            field in the UserInvested model, to hold the total amount invested.
        '''

        user_investment = UserInvestment.objects.filter(user=request.user.profile).last()
        investment_transaction = InvestmentTransaction.objects.get(user_investment=user_investment)

        if success is False:
            Thread(target=send_email.failed_investment_mail, args=[request, investment_transaction]).start()
            data['detail'] = response
            return Response(data, status.HTTP_400_BAD_REQUEST)

        # Inform user that the investment request was successful and it's being reviewed by an admin.
        Thread(target=send_email.awaiting_investment_approval_mail, args=[request]).start()

        # Inform Admin of the requested investment by this user.
        Thread(target=send_email.investment_notification_to_admin, args=[request, investment_transaction]).start()

        data['detail'] = "Investment created successfully"
        data['data'] = UserInvestmentSerializer(response).data
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
            data['data'] = UserInvestmentSerializer(UserInvestment.objects.get(id=investment_id, user=user)).data

        return Response(data)
