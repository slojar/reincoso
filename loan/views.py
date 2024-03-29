import decimal
from threading import Thread
from django.shortcuts import get_object_or_404, reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from account import send_email
from account.send_email import log_request
from savings.models import Saving, SavingTransaction
from rest_framework import status
from django.utils import timezone
from django.utils.timezone import timedelta
from django.contrib.sites.models import Site
from django.conf import settings
from .models import *
from .paginations import CustomPagination
from .serializers import *
from .utils import *
from django.db.models import Q, Sum
from modules.paystack import verify_paystack_transaction
from account.utils import tokenize_user_card

from humanize import intcomma


class ApplyForLoanView(APIView):

    def get(self, request):

        offer = dict()
        duration = request.GET.get("duration")
        amount = request.GET.get("amount")
        loan_basis = request.GET.get("repayment_frequency", "weekly")

        data = dict()
        success, response, requirement, response_code = can_get_loan(request)
        if not success:
            data['detail'] = response
            data['reason'] = requirement
            data['code'] = response_code
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        loan_basis = str(loan_basis).lower()

        success, loan_offer, required, err_code = get_loan_offer(request.user.profile)
        if success is False:
            return Response({
                "detail": loan_offer,
                "reason": required,
                "code": err_code
            }, status=status.HTTP_401_UNAUTHORIZED)

        if amount:
            loan_offer = decimal.Decimal(amount)

        offer['offered_amount'] = amount = loan_offer

        if not duration:
            offer['durations'] = LoanDurationSerializer(LoanDuration.objects.all(), many=True).data
            offer['detail'] = "You are eligible for a loan"
            offer['reason'] = "Eligible"
            offer['code'] = "00"

        if duration:
            try:
                duration = LoanDuration.objects.get(pk=duration)
            except LoanDuration.DoesNotExist:
                return Response({"detail": "Invalid duration selected"}, status=status.HTTP_404_NOT_FOUND)

            offer['duration_title'] = duration.title
            # offer['payment_basis'] = duration.basis
            offer['payment_basis'] = loan_basis
            # offer['payment_duration'] = duration.duration
            repayment_count = calculate_loan_repayment_duration(loan_basis, duration)
            offer['payment_duration'] = repayment_count
            offer['percentage'] = duration.percentage
            offer['total_percentage'] = total_percentage = (amount * duration.percentage) / 100
            offer['total_repayment'] = total_repayment = amount + total_percentage
            # split = round(total_repayment / duration.duration, 2)
            split = round(total_repayment / repayment_count, 2)
            payment_split = list()
            # for payment_duration in range(duration.duration):
            for payment_duration in range(repayment_count):
                payment_split.append({
                    'amount': split
                })
            offer['repayment_split'] = payment_split
            # offer['detail'] = f"You pay {split} for {repayment_count} {loan_basis[:-2]}(s)"
            naira_unicode = settings.NAIRA_UNICODE
            offer['detail'] = f"You pay {naira_unicode}{intcomma(split, 2)} for {repayment_count} {loan_basis[:-2]}(s)"
            offer['reason'] = "Eligible"
            offer['code'] = "00"

        # print("success on loa")
        return Response(offer)

    def post(self, request):

        data = dict()
        amount = request.data.get('amount')
        duration_id = request.data.get('duration')

        if amount < 1000000:
            return Response({"detail": "Requested amount cannot be less than One Million Naira (N1,000,000)"},
                            status=status.HTTP_404_NOT_FOUND)

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

        success, response, requirement, response_code = can_get_loan(request)
        if not success:
            data['detail'] = response
            data['reason'] = requirement
            data['code'] = response_code
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

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

        log_request(request.data, data)

        return Response(data)


class LoanDurationView(ListAPIView):
    permission_classes = []
    serializer_class = LoanDurationSerializer
    queryset = LoanDuration.objects.all().order_by('id')


class LoanView(ListAPIView):
    serializer_class = LoanSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        query = Loan.objects.filter(user=self.request.user.profile)
        return query

    def list(self, request, *args, **kwargs):
        data = super(LoanView, self).list(request, *args, **kwargs).data
        profile = request.user.profile
        user_loan_info = dict()
        user_loan_info['total_loan'] = Loan.objects.filter(user=profile).count()

        total = LoanTransaction.objects.filter(user=profile, status='success')
        total = total.aggregate(Sum('amount'))['amount__sum']
        user_loan_info['total_loan_amount'] = str(total)

        data['loan_analysis'] = user_loan_info

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
        
        # Send email to user for loan repayment confirmation
        loan = get_object_or_404(Loan, id=loan_id, user=request.user.profile)
        if success and loan.status == 'repaid':
            Thread(target=loan_clear_off, args=[request, amount]).start()
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


