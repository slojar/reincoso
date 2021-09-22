from account.serializers import *
from account.utils import signup, reformat_phone_number
from loan.serializers import *
from loan.paginations import CustomPagination
from savings.serializers import *
from investment.serializers import *
from settings.serializers import *
from account.utils import encrypt_text

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser

from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password


class AdminHomepage(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        data = dict()
        data['total_feedback'] = FeedbackMessage.objects.all().count()
        data['total_user'] = User.objects.all().count()
        data['total_investment'] = Investment.objects.all().count()
        data['total_loan'] = Loan.objects.all().count()
        data['active_loan'] = Loan.objects.filter(status='ongoing').count()
        data['declined_loan'] = Loan.objects.filter(status='unapproved').count()
        data['pending_loan'] = Loan.objects.filter(status='pending').count()
        data['fully_repaid_loan'] = Loan.objects.filter(status='repaid').count()
        data['total_saving'] = Saving.objects.all().count()
        data['total_saving_transaction'] = SavingTransaction.objects.all().count()
        data['pending_saving_transaction'] = SavingTransaction.objects.filter(status='pending').count()
        data['successful_saving_transaction'] = SavingTransaction.objects.filter(status='success').count()
        data['failed_saving_transaction'] = SavingTransaction.objects.filter(status='failed').count()
        data['total_loan_transaction'] = LoanTransaction.objects.all().count()
        data['pending_loan_transaction'] = LoanTransaction.objects.filter(status='pending').count()
        data['unsuccessful_loan_transaction'] = LoanTransaction.objects.filter(status='unsuccessful').count()
        data['cancelled_loan_transaction'] = LoanTransaction.objects.filter(status='cancelled').count()
        data['successful_loan_transaction'] = LoanTransaction.objects.filter(status='success').count()

        return Response(data)


class AdminFaqView(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = FaqSerializer
    queryset = Faq.objects.all()
    lookup_field = 'id'


class AdminFaqCategoryView(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = FaqCategorySerializer
    queryset = FaqCategory.objects.all()
    lookup_field = 'id'


class AdminFeedbackMessageView(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = FeedbackMessageSerializer
    queryset = FeedbackMessage.objects.all()
    lookup_field = 'id'


class AdminProfileViewOld(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = UserDetailSerializer
    queryset = Profile.objects.all()
    lookup_field = 'id'


class AdminLoanDurationView(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = LoanDurationSerializer
    queryset = LoanDuration.objects.all()
    lookup_field = 'id'


class AdminLoanTransactionView(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = LoanTransactionSerializer
    queryset = LoanTransaction.objects.all()
    lookup_field = 'id'


class AdminSavingDurationView(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = SavingDurationSerializer
    queryset = Duration.objects.all()
    lookup_field = 'id'


class AdminSavingTransactionView(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = SavingTransactionSerializer
    queryset = SavingTransaction.objects.all()
    lookup_field = 'id'


class AdminInvestmentOptionView(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = InvestmentOptionSerializer
    queryset = InvestmentOption.objects.all()
    lookup_field = 'id'


class AdminInvestmentSpecificationView(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = InvestmentSpecificationSerializer
    queryset = InvestmentSpecification.objects.all()
    lookup_field = 'id'


class AdminGeneralSettingView(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = GeneralSettingsSerializer
    queryset = GeneralSettings.objects.all()
    lookup_field = 'id'


class AdminPaymentGatewayView(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = PaymentGatewaySerializer
    queryset = PaymentGateway.objects.all()
    lookup_field = 'id'
    
    
class AdminLoanSettingView(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = LoanSettingSerializer
    queryset = LoanSetting.objects.all()
    lookup_field = 'id'


class AdminSiteView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = SiteSerializer
    queryset = Site.objects.all()


class AdminInvestmentDurationView(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = InvestmentDurationSerializer
    queryset = InvestmentDuration.objects.all()
    lookup_field = 'id'


class AdminProfileView(APIView, CustomPagination):
    permission_classes = [IsAdminUser]

    def get(self, request, profile_id=None):
        if profile_id:
            user = Profile.objects.get(id=profile_id)
            serializer = UserDetailSerializer(user).data
        else:
            user = Profile.objects.all()
            user = self.paginate_queryset(user, request)
            user = UserDetailSerializer(user, many=True).data
            serializer = self.get_paginated_response(user).data
        return Response(serializer)

    def post(self, request):
        data = dict()
        success, detail = signup(request)
        data['success'] = success
        data['detail'] = detail
        if not success:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(data)

    def put(self, request, profile_id):
        try:
            phone_number = request.data.get('phone_number')

            profile = get_object_or_404(Profile, id=profile_id)
            profile.user.first_name = request.data.get('first_name')
            profile.user.last_name = request.data.get('last_name')
            profile.user.email = request.data.get('email')
            profile.gender = request.data.get('gender')
            profile.paid_membership_fee = request.data.get('paid_membership_fee')
            profile.status = request.data.get('status')
            if phone_number:
                phone_number = reformat_phone_number(phone_number)
                profile.user.username = phone_number
                profile.user.password = make_password(phone_number)
                profile.phone_number = phone_number

            profile.user.save()
            profile.save()
            data = UserDetailSerializer(profile).data
            return Response(data)
        except Exception as ex:
            return Response({'detail': str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, profile_id):
        try:
            profile = get_object_or_404(Profile, id=profile_id)
            profile.delete()
            return Response({'detail': 'profile deleted successfully'})
        except Exception as ex:
            return Response({'detail': str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class AdminAvailableInvestmentView(ModelViewSet):
    permission_classes = []
    serializer_class = AvailableInvestmentSerializer
    queryset = AvailableInvestment.objects.all()
    lookup_field = 'id'



