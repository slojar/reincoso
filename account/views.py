from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from modules.paystack import get_paystack_link
from .serializers import *
from .utils import *
from django.contrib.auth import authenticate
from settings.utils import general_settings
from transaction.models import Transaction


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
        data['data'] = UserDetailSerializer(user.profile).data
        return Response(data, status=status.HTTP_200_OK)


class UserDetailView(APIView):

    def get(self, request):
        data = UserDetailSerializer(request.user.profile).data
        return Response(data)


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


class PayMembershipFeeView(APIView):

    def post(self, request):
        data = dict()
        site_settings = general_settings()
        gateway = request.data.get('gateway')
        callback_url = request.data.get('callback_url')

        if not callback_url:
            callback_url = f"{request.scheme}://{request.get_host()}{request.path}"
        callback_url = callback_url + f"?gateway={gateway}"

        email = request.user.email
        profile = request.user.profile
        amount = site_settings.membership_fee

        # create transaction for membership payment
        trans, created = Transaction.objects.get_or_create(user=request.user.profile, transaction_type='membership fee', status='pending')
        trans.payment_method = gateway
        trans.amount = amount
        trans.save()

        metadata = {
            'transaction_id': trans.id,
            'payment_for': 'membership fee',
        }

        if gateway == 'paystack':
            success, response = get_paystack_link(email=email, amount=amount, callback_url=callback_url, metadata=metadata)
            if success:
                data['payment_link'] = response
                data['membership_id'] = profile.member_id
                profile.paid_membership_fee = True
                profile.save()
            else:
                data['detail'] = response

        return Response(data)


class AddGuarantorView(APIView):

    def post(self, request):
        guarantor = request.data.get('guarantor')
        response = []
        for number in guarantor:
            try:
                guarantor = Profile.objects.get(phone_number=reformat_phone_number(number))
                guarantor, created = Guarantor.objects.get_or_create(user=request.user.profile, guarantor=guarantor)
                if not created:
                    response.append({
                        'success': False,
                        'phone_number': number,
                        'detail': 'This user is already your guarantor',
                    })

                if created:
                    response.append({
                        'success': True,
                        'phone_number': number,
                        'detail': 'Guarantor added successfully',
                    })

                    # send notification to guarantor

            except Profile.DoesNotExist:
                response.append({
                    'success': False,
                    'phone_number': number,
                    'detail': 'Phone number not registered',
                })

        return Response(response)


class UpdateGuarantorView(APIView):

    def put(self, request):
        data = dict()
        phone_number = request.data.get('user')
        confirm = request.data.get('confirm')
        if phone_number:
            phone_number = reformat_phone_number(phone_number)

        if not Profile.objects.filter(phone_number=phone_number).exists():
            data['detail'] = 'This phone is not registered'
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        profile = Profile.objects.get(phone_number=phone_number)

        if not Guarantor.objects.filter(user=profile, guarantor=request.user.profile).exists():
            data['detail'] = 'This user did not make you a guarantor'
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

        guarantor = Guarantor.objects.get(user=profile, guarantor=request.user.profile)
        if confirm is True:
            guarantor.confirmed = True
            # notify user of guarantor's confirmation
        else:
            guarantor.confirmed = False
        guarantor.save()

        data['detail'] = "Confirmation successful"
        return Response(data)

