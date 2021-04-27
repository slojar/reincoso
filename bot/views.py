from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView
from .serializers import *
from .utils import *
from transaction.models import SavingTransaction
from django.contrib.auth import authenticate
from datetime import datetime, timedelta


class SignupView(APIView):
    permission_classes = []

    def post(self, request):
        data = dict()
        success, detail, response = signup(request)
        data['success'] = success
        data['detail'] = detail
        return Response(data, status=response)


class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        phone_number = request.data.get('phone_number')

        data = dict()
        data['success'] = False
        if not phone_number:
            data['detail'] = 'Phone number not provided'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            phone_number = f"234{phone_number[-10:]}"
        if not User.objects.filter(username=phone_number).exists():
            data['detail'] = 'Account with this phone number does not exist'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=phone_number, password=phone_number)

        token = Token.objects.get(user__username=phone_number)
        token.delete()
        token = Token.objects.create(user=user)

        if not user:
            data['detail'] = 'Wrong phone number provided'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        data['success'] = True
        data['detail'] = 'Login successful'
        data['token'] = token.key
        return Response(data, status=status.HTTP_200_OK)


class FaqView(ListAPIView):
    permission_classes = []
    pagination_class = PageNumberPagination
    serializer_class = FaqSerializer
    queryset = Faq.objects.all()


class FeedbackMessageView(ListCreateAPIView):
    permission_classes = []
    pagination_class = PageNumberPagination
    serializer_class = FeedbackMessageSerializer
    queryset = FeedbackMessage.objects.all()


class FeedbackMessageDetailView(RetrieveAPIView):
    permission_classes = []
    pagination_class = PageNumberPagination
    serializer_class = FeedbackMessageSerializer
    queryset = FeedbackMessage.objects.all()
    lookup_field = 'id'


class PayMembershipView(APIView):
    def post(self, request):
        data = dict()
        gateway = request.data.get('gateway')
        callback_url = request.data.get('callback_url')

        if not callback_url:
            callback_url = f"{request.scheme}://{request.get_host()}{request.path}"
        callback_url = callback_url + f"?gateway={gateway}"

        email = request.user.email
        profile = request.user.profile
        amount = 1000000

        if gateway == 'paystack':
            success, response = get_paystack_link(email=email, amount=amount, callback_url=callback_url)
            if success:
                data['payment_link'] = response
                data['membership_id'] = profile.member_id
                profile.paid_membership_fee = True
                profile.save()
            else:
                data['detail'] = response

        return Response(data)


class SavingsView(APIView):
    def post(self, request):
        data = dict()
        amount = request.data.get('amount')
        fixed_payment = request.data.get('fixed_payment')
        repayment_day = request.data.get('repayment_day')
        gateway = request.data.get('gateway')
        callback_url = request.data.get('callback_url')
        payment_duration_id = request.data.get('payment_duration_id')

        if not Duration.objects.filter(id=payment_duration_id).exists():
            data['detail'] = 'Invalid payment duration'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        email = request.user.email
        payment_duration_id = Duration.objects.get(id=payment_duration_id)

        if not callback_url:
            callback_url = f"{request.scheme}://{request.get_host()}{request.path}"
        callback_url = callback_url + f"?gateway={gateway}"

        if fixed_payment:
            amount = fixed_payment

        # Create/Update Saving Account
        saving, created = Saving.objects.get_or_create(user=request.user.profile)
        saving.duration = payment_duration_id
        saving.last_payment = amount
        saving.fixed_payment = fixed_payment
        saving.last_payment_date = datetime.now()
        saving.balance = saving.balance + amount
        saving.repayment_day = repayment_day

        # Calculate next repayment date
        last_date = saving.last_payment_date
        duration_interval = saving.duration.interval
        next_date = last_date + timedelta(days=duration_interval)
        saving.next_payment_date = next_date
        saving.save()

        # Create saving transaction
        transaction, created = SavingTransaction.objects.get_or_create(user=request.user.profile,
                                                                       saving_id=saving.id, status='pending')
        transaction.payment_method = gateway
        transaction.amount = amount
        transaction.save()

        if gateway == 'paystack':
            metadata = {
                "transaction_id": transaction.id,
            }
            success, response = get_paystack_link(email=email, amount=amount, callback_url=callback_url,
                                                  metadata=metadata)
            if success:
                data['payment_link'] = response
            else:
                data['detail'] = response

        return Response(data)


