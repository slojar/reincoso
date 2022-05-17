import decimal
from threading import Thread
from django.shortcuts import get_object_or_404, reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from account import send_email
from savings.models import Saving, SavingTransaction
from rest_framework import status
from django.utils import timezone
from django.utils.timezone import timedelta
from django.contrib.sites.models import Site
from .models import *
from .paginations import CustomPagination
from .serializers import *
from .utils import *
from django.db.models import Q, Sum
from modules.paystack import verify_paystack_transaction
from account.utils import tokenize_user_card


class ApplyForLoanView(APIView):

    def get(self, request):
        offer = dict()
        duration = request.GET.get("duration")
        amount = request.GET.get("amount")
        success, loan_offer = get_loan_offer(request.user.profile)
        if success is False:
            return Response({"detail": loan_offer}, status=status.HTTP_401_UNAUTHORIZED)

        if amount:
            loan_offer = decimal.Decimal(amount)

        offer['offered_amount'] = amount = loan_offer

        if not duration:
            offer['durations'] = LoanDurationSerializer(LoanDuration.objects.all(), many=True).data

        if duration:
            try:
                duration = LoanDuration.objects.get(pk=duration)
            except LoanDuration.DoesNotExist:
                return Response({"detail": "Invalid duration selected"}, status=status.HTTP_404_NOT_FOUND)

            offer['duration_title'] = duration.title
            offer['payment_basis'] = duration.basis
            offer['payment_duration'] = duration.duration
            offer['percentage'] = duration.percentage
            offer['total_percentage'] = total_percentage = (amount * duration.percentage) / 100
            offer['total_repayment'] = total_repayment = amount + total_percentage
            split = round(total_repayment / duration.duration, 2)
            payment_split = list()
            for payment_duration in range(duration.duration):
                payment_split.append({
                    'amount': split
                })
            offer['repayment_split'] = payment_split
            offer['detail'] = f"You pay {split} for {duration.duration} {duration.basis[:-2]}(s)"
        # print("success on loa")
        return Response(offer)

    def post(self, request):
        data = dict()
        amount = request.data.get('amount')
        duration_id = request.data.get('duration')

        try:
            duration = LoanDuration.objects.get(pk=duration_id)
        except LoanDuration.DoesNotExist:
            return Response({"detail": "Invalid duration selected"}, status=status.HTTP_404_NOT_FOUND)

        success, loan_offer = get_loan_offer(request.user.profile)
        if success is False:
            return Response({"detail": loan_offer}, status=status.HTTP_401_UNAUTHORIZED)

        if not amount:
            amount = loan_offer

        # check if amount is not greater than loan offer amount
        if decimal.Decimal(amount) > float(loan_offer):
            data['detail'] = f"You cannot get loan more than the offered amount of {loan_offer}"
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

        success, response, requirement = can_get_loan(request.user.profile)
        if not success:
            if not success:
                data['detail'] = response
                data['code'] = requirement
                return Response(data, status=status.HTTP_401_UNAUTHORIZED)

        profile = request.user.profile
        success, response = create_loan(request, profile, amount, duration)
        if not success:
            data['detail'] = response
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

        data['detail'] = response

        # Mail to User
        Thread(target=send_email.loan_request_processing_mail, args=[request]).start()

        # Mail to Admin
        Thread(target=send_email.admin_loan_processing_status_mail, args=[request]).start()
        
        return Response(data)


class LoanDurationView(ListAPIView):
    permission_classes = []
    serializer_class = LoanDurationSerializer
    queryset = LoanDuration.objects.all()


class LoanView(ListAPIView):
    serializer_class = LoanSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        query = Loan.objects.filter(user=self.request.user.profile)
        return query

    def list(self, request, *args, **kwargs):
        data = super(LoanView, self).list(request, *args, **kwargs).data
        profile = request.user.profile
        user_info = dict()
        user_info['total_loan'] = Loan.objects.filter(user=profile).count()

        total = LoanTransaction.objects.filter(user=profile, status='success')
        total = total.aggregate(Sum('amount'))['amount__sum']
        user_info['total_loan_amount'] = total

        data['user'] = user_info

        return Response(data)


class LoanDetailView(RetrieveAPIView):
    serializer_class = LoanSerializer
    lookup_field = 'pk'
    queryset = Loan.objects.all()


class LoanTransactionView(ListAPIView):
    serializer_class = LoanTransactionSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        loan_id = self.kwargs.get('loan_id')
        return LoanTransaction.objects.filter(loan_id=loan_id)


class LoanTransactionDetailView(RetrieveAPIView):
    serializer_class = LoanTransactionSerializer
    lookup_field = 'pk'
    queryset = LoanTransaction.objects.all()


class RepayLoanView(APIView):

    def post(self, request):
        data = dict()
        action = request.data.get('action')
        amount = request.data.get('amount')
        loan_id = request.data.get('loan_id')
        card_id = request.data.get('card_id')
        callback_url = request.data.get('callback_url')
        gateway = request.data.get('payment_gateway')

        if not callback_url:
            url = reverse("loan:verify-payment")
            callback_url = f"{request.scheme}://{request.get_host()}{url}?gateway={gateway}"

        if not amount or float(amount) <= 0:
            data['detail'] = 'amount is required'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        success, response = do_loan_repayment(request.user.profile, loan_id, amount, card_id=card_id,
                                              request=request, callback_url=callback_url)
        data['detail'] = response
        if not card_id:
            data['redirect'] = True
        if success is False:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        return Response(data)


class VerifyLoanPaymentView(APIView):
    permission_classes = []

    def get(self, request):
        data = dict()
        gateway = request.GET.get('gateway')
        reference = request.GET.get('reference')

        if not gateway or reference:
            data['detail'] = 'Error in request, please specify a gateway and a reference number'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        success, response = verify_loan_repayment(gateway, reference)
        data['detail'] = response

        if success is False:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        return Response(data)


