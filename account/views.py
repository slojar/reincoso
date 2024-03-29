from decimal import Decimal

from django.shortcuts import render
from django.contrib import messages

from django.contrib.admin.models import LogEntry
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from modules.paystack import get_paystack_link
from django.contrib.contenttypes.models import ContentType

from superadmin.models import AdminNotification
from .serializers import *
from .utils import *
from django.contrib.auth import authenticate
from settings.utils import general_settings
from transaction.models import Transaction
import logging
from django.conf import settings
from .send_email import *
from threading import Thread

log = logging.getLogger(__name__)


class Homepage(APIView):
    permission_classes = []

    def get(self, request):
        log.info("Homepage")
        return HttpResponse('<h1>Reincoso Homepage!!!</h1>')


class SignupView(APIView):
    permission_classes = []

    def post(self, request):
        data = dict()
        success, detail = signup(request)
        data['success'] = success
        data['detail'] = detail
        if not success:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        return Response(data)


class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        phone_number = request.data.get('phone_number')
        login_type = request.data.get('login_type')

        data = dict()
        data['success'] = False
        if not phone_number:
            data['detail'] = 'Phone number not provided'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        if login_type:
            phone_number = 'admin'
        else:
            phone_number = f"234{phone_number[-10:]}"
        if not User.objects.filter(username=phone_number).exists():
            data['detail'] = 'Account with this phone number does not exist'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=phone_number, password=phone_number)
        if not user:
            data['detail'] = 'Wrong phone number provided'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        if Group.objects.filter(user=user).exists():
            LogEntry.objects.log_action(user_id=user.id, content_type_id=ContentType.objects.get_for_model(User).pk,
                                        change_message='Logged in', object_repr=f'', object_id='', action_flag=2)

        data['success'] = True
        data['detail'] = 'Login successful'
        data['token'] = str(RefreshToken.for_user(user).access_token)
        if not login_type:
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
        data = pay_membership(request)
        return Response(data)


def confirm_guarantorship(request):
    """
    :info: confirmation view for guarantorship
        This will later call the UpdateGuarantorView view.
    :param request:
    :return:
    """
    try:
        confirmed: bool = False
        response = "Select Yes / No to Accept or Decline Guarantor-ship"
        if request.method == "GET":
            guarantor, guarantee = request.GET.get('guarantor'), request.GET.get('guarantee')
            response = messages.info(request, "Select Yes / No to Accept or Decline Guarantor-ship")
            if not all([guarantor, guarantee]):
                response = messages.error(request, "Incorrect/Missing Fields")

            if not (guarantor[0:3] == "234" and guarantee[0:3] == "234"):
                response = messages.error(request, "Invalid Guarantor/Guarantee Phone Number")

            guarantor_profile = Profile.objects.get(phone_number=guarantor)
            guarantee_profile = Profile.objects.get(phone_number=guarantee)

            if not Guarantor.objects.filter(user=guarantee_profile, guarantor=guarantor_profile).exists():
                response = messages.error(request, f"You don't have a request for being a Guarantor to {guarantee}")

            confirmed = Guarantor.objects.get(user=guarantee_profile, guarantor=guarantor_profile).confirmed
            return render(request, 'account/accept_or_decline.html', {"response": response, "confirmed": confirmed,
                                                                      "guarantee": guarantee})

        if request.method == "POST":
            guarantor, guarantee = request.GET.get('guarantor'), request.GET.get('guarantee')
            if not all([guarantor, guarantee]):
                response = messages.error(request, "Incorrect/Missing Fields")

            guarantor_profile = Profile.objects.get(phone_number=guarantor)
            guarantee_profile = Profile.objects.get(phone_number=guarantee)

            user = User.objects.get(username=guarantee)

            if request.POST.get("submit") == "CONFIRM" and request.POST.get("confirm") == 'True':
                instance = Guarantor.objects.get(user=guarantee_profile, guarantor=guarantor_profile)
                instance.confirmed = True
                instance.save()
                confirmed = True
                # send mail to guarantee on guarantor's acceptance

                response = messages.success(request, f"You have successfully accepted to become a Guarantor to"
                                                     f" {guarantee}")
                Thread(target=guarantor_accept_mail, args=[user, guarantor]).start()

            if request.POST.get("submit") == "CONFIRM" and request.POST.get("confirm") == 'False':
                instance = Guarantor.objects.get(user=guarantee_profile, guarantor=guarantor_profile)
                instance.confirmed = False
                instance.save()
                confirmed = False
                response = messages.info(request, f"You have Declined to become a Guarantor to {guarantee}")

                # send mail to guarantee on guarantor's decline
                Thread(target=guarantor_declined_mail, args=[user, guarantor]).start()

        return render(request, 'account/confirm.html', {"response": response, "confirmed": confirmed,
                                                        "guarantee": guarantee})

    except (Exception,) as err:
        response = messages.error(request, "Something went wrong")
        return render(request, 'account/accept_or_decline.html', {"response": response})


class AddGuarantorView(APIView):

    def post(self, request):
        guarantor = request.data.get('requestNumber')
        amount = request.data.get('amount')
        response = []
        for number in guarantor:
            try:
                guarantor_profile = Profile.objects.get(phone_number=reformat_phone_number(str(number).strip()))
                guarantor, created = Guarantor.objects.get_or_create(user=request.user.profile,
                                                                     guarantor=guarantor_profile)
                guarantor.confirmed = False
                guarantor.save()
                # if not created:
                #     response.append({
                #         'success': False,
                #         'phone_number': number,
                #         'detail': 'This user is already your guarantor',
                #     })
                # if created:
                #     response.append({
                #         'success': True,
                #         'phone_number': number,
                #         'detail': 'Guarantor added successfully',
                #     })

                response.append({
                    'success': True,
                    'phone_number': number,
                    'detail': 'Guarantor added successfully',
                })

                # send notification to guarantor
                Thread(target=mail_to_guarantor, args=[request, guarantor_profile, amount]).start()
            except Profile.DoesNotExist:
                response.append({
                    'success': False,
                    'phone_number': number,
                    'detail': 'Phone number not registered',
                })

        # send mail to user
        if response[0].get("success") is True:
            Thread(target=inform_user_of_added_guarantor, args=[request]).start()

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


class GetBankView(ListAPIView):
    permission_classes = []
    serializer_class = BankSerializer

    def get_queryset(self):
        queryset = Bank.objects.all().order_by('id')
        name = self.request.GET.get('name')
        if name:
            queryset = Bank.objects.filter(name__icontains=name)
        return queryset


class RequestWithdrawalView(APIView):

    def post(self, request):
        user = request.user

        amount = request.data.get('amount', '')
        description = request.data.get('reason', '')

        if not amount:
            return Response({"detail": "Amount is required"}, status=status.HTTP_400_BAD_REQUEST)

        if Withdrawal.objects.filter(requested_by=user, status='pending').exists():
            return Response({"detail": "You have a pending withdrawal, please contact admin"},
                            status=status.HTTP_400_BAD_REQUEST)

        new_amount = str(amount).replace(",", "")

        user_wallet_balance = user.profile.wallet.balance

        if Decimal(new_amount) > user_wallet_balance:
            return Response({"detail": "Amount cannot be greater than your total balance"},
                            status=status.HTTP_400_BAD_REQUEST)

        withdrawal = Withdrawal.objects.create(requested_by=user)
        withdrawal.amount = Decimal(new_amount)
        withdrawal.description = description
        withdrawal.save()

        # Notification for admin
        content = f"""
        Dear Admin,
        A user {request.user.first_name} {request.user.last_name} has requested a withdrawal,
        Please check and act accordingly.
        """
        notification = AdminNotification.objects.create(message=content)
        # Email admin.
        Thread(target=withdrawal_request_mail_admin, args=[request, content]).start()

        # Email user.
        Thread(target=withdrawal_request_mail_user, args=[request]).start()
        return Response({"detail": "Your withdrawal request is being processed"})
