from ast import arg
import logging
from datetime import datetime, timedelta
from threading import Thread
from django.conf import settings

from django.db.models import Sum
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView

from loan.paginations import CustomPagination
from savings.models import Duration, Saving, SavingTransaction
from .serializers import *
from settings.models import PaymentGateway
from modules.paystack import verify_paystack_transaction
from modules.paystack import get_paystack_link
from account.utils import tokenize_user_card
from account.models import UserCard
from modules.paystack import paystack_auto_charge
from transaction.models import Transaction
from investment.utils import approve_investment
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from account import send_email 
from .utils import get_savings_analysis, create_instant_savings, create_auto_savings, update_savings_payment

# from account.send_email import failed_membership_fee_payment, successful_membership_fee_payment

class MySavingsView(ListAPIView):
    serializer_class = SavingSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        profile = self.request.user.profile
        query = Saving.objects.filter(user=profile)
        return query

    def list(self, request, *args, **kwargs):
        profile = self.request.user.profile
        data = super(MySavingsView, self).list(request, *args, **kwargs).data
        data['user'] = get_savings_analysis(profile)
        return Response(data)


class MySavingsDetailView(RetrieveAPIView):
    serializer_class = SavingSerializer

    def get(self, request, pk):
        profile = request.user.profile
        savings = get_object_or_404(Saving, pk=pk, user=profile)
        data = SavingSerializer(savings).data
        data['user'] = get_savings_analysis(profile)
        return Response(data)


class SavingTransactionView(ListAPIView):
    serializer_class = SavingsTransactionSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        savings_id = self.kwargs.get('savings_id')
        return SavingTransaction.objects.filter(saving_id=savings_id)

    def list(self, request, *args, **kwargs):
        profile = request.user.profile
        data = super(SavingTransactionView, self).list(request, *args, **kwargs).data
        data['user'] = get_savings_analysis(profile)
        return Response(data)


class SavingTransactionDetailView(RetrieveAPIView):
    serializer_class = SavingsTransactionSerializer
    lookup_field = 'pk'
    queryset = SavingTransaction.objects.all()

    def get(self, request, pk):
        profile = request.user.profile
        data = super(SavingTransactionDetailView, self).get(request).data
        data['user'] = get_savings_analysis(profile)
        return Response(data)


class SavingsView(APIView):

    def get(self, request):
        data = dict()
        profile = request.user.profile
        data['user'] = get_savings_analysis(profile)
        data['savings_types'] = SavingsTypeSerializer(SavingsType.objects.filter(active=True), many=True).data
        data['durations'] = SavingDurationSerializer(Duration.objects.all(), many=True).data
        data['gateways'] = PaymentGateway.objects.all().values('id', 'name', 'slug')
        return Response(data)

    def post(self, request):
        success = False
        response = ""
        data = dict()
        savings_type = request.data.get('savings_type')

        try:
            savings_type = SavingsType.objects.get(id=savings_type)
        except Exception as ex:
            data['detail'] = f"{ex}"
            return Response(data, status.HTTP_400_BAD_REQUEST)
        
        profile = Profile.objects.get(user=request.user)
        saving_amount = Saving.objects.filter(user=profile).last()

        if savings_type.slug == 'auto':
            success, response = create_auto_savings(savings_type=savings_type, request=request)

            if success:
                Thread(target=send_email.successful_auto_save_mail, args=[profile]).start()
            else:
                Thread(target=send_email.failed_auto_save_mail, args=[profile]).start()


        if savings_type.slug == 'instant':
            success, response = create_instant_savings(savings_type=savings_type, request=request)

            if success:
                Thread(target=send_email.successful_quick_save_mail, args=[profile]).start()
            else:
                Thread(target=send_email.failed_quick_save_mail, args=[profile]).start()

        data['detail'] = response
        data['payment_link'] = response
        if not success:
            return Response(data, status.HTTP_400_BAD_REQUEST)

        return Response(data)


class VerifyPaymentView(APIView):
    permission_classes = []

    def get(self, request):
        data = dict()
        gateway = request.GET.get('gateway')
        reference = request.GET.get('reference')
        phone_number = None
        success = False
        response = dict()

        if gateway == 'paystack':
            success, response = verify_paystack_transaction(reference)
            data['detail'] = response

            if success is False:
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            # tokenize card
            tokenize_user_card(response, gateway)

            amount = response['amount']
            email = response['email']
            transaction_id = response['payload']['data']['metadata'].get('transaction_id', None)
            payment_for = response['payload']['data']['metadata'].get('payment_for', None)
            profile = Profile.objects.get(user__email__iexact=email)
            phone_number = profile.phone_number

            if payment_for == 'membership fee':
                trans = Transaction.objects.get(id=transaction_id, transaction_type=payment_for)
                trans.reference = reference
                trans.status = 'success'
                trans.response = response
                profile.paid_membership_fee = True
                profile.save()
                trans.save()

            if payment_for == 'savings':
                trans = SavingTransaction.objects.get(id=transaction_id, user__user__email__iexact=email)

                trans.reference = reference
                if trans.status != 'success':
                    trans.status = 'success'
                    saving = update_savings_payment(saving=trans.saving, amount=amount)

                trans.response = response
                trans.save()

            if payment_for == 'investment':
                investment_id = response['payload']['data']['metadata'].get('investment_id', None)
                success, response = approve_investment(investment_id, gateway, reference)
                data['detail'] = response
                if success is False:
                    return Response(data, status.HTTP_400_BAD_REQUEST)
                # return Response(data)

        if success is False:
            data['detail'] = "Transaction could not be verified at the moment"

            # Send Transaction Failure mail

            if payment_for == "membership fee":
                Thread(target=send_email.failed_membership_fee_payment, args=[trans]).start()

            if payment_for == 'savings':
                ...

            if payment_for == 'investment':
                ...
        else:

            # Send Transaction Success Mail

            if payment_for == "membership fee":
                Thread(target=send_email.successful_membership_fee_payment, args=[trans]).start()

            if payment_for == 'savings':
                ...

            if payment_for == 'investment':
                ...

            data['detail'] = "Transaction successful"

        data['msisdn'] = phone_number
        return Response(data)


