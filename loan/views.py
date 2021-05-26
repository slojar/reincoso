import decimal
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from savings.models import Saving, SavingTransaction
from rest_framework import status
from django.utils import timezone
from django.utils.timezone import timedelta
from django.contrib.sites.models import Site
from .models import *
from .serializers import *
from .utils import *
from django.db.models import Q


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

        if decimal.Decimal(amount) > float(loan_offer):
            data['detail'] = f"You cannot get loan more than the offered amount of {loan_offer}"
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

        success, response, requirement = can_get_loan(request.user.profile)
        if not success:
            if not success:
                data['detail'] = response
                data['requirement'] = requirement
                return Response(data, status=status.HTTP_401_UNAUTHORIZED)

        success, response = create_loan(profile=request.user.profile, amount=amount, duration=duration)
        if not success:
            data['detail'] = response
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

        data['detail'] = response
        return Response(data)


class LoanDurationView(ListAPIView):
    permission_classes = []
    serializer_class = LoanDurationSerializer
    queryset = LoanDuration.objects.all()


class LoanView(APIView):

    def get(self, request, pk=None):
        if not pk:
            data = LoanSerializer(Loan.objects.filter(user=request.user.profile), many=True).data
        else:
            data = LoanSerializer(get_object_or_404(Loan, pk=pk, user=request.user.profile)).data
        return Response(data)


class RepayLoanView(APIView):

    def post(self, request):
        data = dict()
        action = request.data.get('action')
        amount = request.data.get('amount')
        loan_id = request.data.get('loan_id')
        card_id = request.data.get('card_id')

        if not amount or float(amount) <= 0:
            data['detail'] = 'amount is required'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        success, response = process_loan_repayment(request.user.profile, loan_id, amount, card_id=card_id)
        data['detail'] = response
        if success is False:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        return Response(data)


