import decimal
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
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

        if not amount:
            amount = loan_offer

        if decimal.Decimal(amount) > loan_offer:
            data['detail'] = f"You cannot get loan more than the offered amount of {loan_offer}"
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

        query = Q(user=request.user.profile)
        exclude = Q(status='unapproved') | Q(status='repaid')
        if Loan.objects.filter(query).exclude(exclude).exists():
            data['detail'] = f"You cannot apply for a loan at the moment because you still have a loan running on your account."
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

        success, response = create_loan(profile=request.user.profile, amount=amount, duration=duration)
        if not success:
            data['detail'] = response
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        data['detail'] = response
        return Response(data)



