from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import *
from .utils import *
from django.contrib.auth import authenticate


class SignupView(APIView):
    permission_classes = []

    def post(self, request):
        data = dict()
        success, detail = signup(request)
        if not success:
            data['detail'] = detail
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        data['detail'] = detail
        return Response(data)


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
        if not user:
            data['detail'] = 'Wrong phone number provided'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        data['success'] = True
        data['detail'] = 'Login successful'
        data['token'] = str(RefreshToken.for_user(user).access_token)
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


