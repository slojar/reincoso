from account.serializers import *
from account.utils import signup, reformat_phone_number
from loan.serializers import *
from loan.paginations import CustomPagination
from savings.serializers import *
from investment.serializers import *
from settings.serializers import *
from .filters import *
from account.utils import encrypt_text

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser

from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


class AdminHomepage(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        data = dict()
        data['total_feedback'] = FeedbackMessage.objects.all().count()
        data['total_user'] = User.objects.all().count()
        data['total_investment'] = UserInvestment.objects.all().count()
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


class AdminAvailableInvestmentView(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = InvestmentSerializer
    queryset = Investment.objects.all()
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


class AdminInvestmentOptionView(APIView, CustomPagination):
    permission_classes = [IsAdminUser]

    def get(self, request, pk=None):
        try:
            if pk:
                option = InvestmentOption.objects.get(id=pk)
                option = InvestmentOptionSerializer(option).data
            else:
                option = InvestmentOption.objects.all().order_by('-id')
                option = self.paginate_queryset(option, request)
                data = InvestmentOptionSerializer(option, many=True).data
                option = self.get_paginated_response(data).data
            return Response(option)
        except Exception as ex:
            return Response({'detail': str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        name = request.data.get('name')
        status = request.data.get('status')
        available_investment = request.data.get('available_investment')
        durations = request.data.get('duration')

        if not name:
            return Response({'detail': "name is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not available_investment:
            return Response({'detail': "available_investment is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not durations:
            return Response({'detail': "duration is required"}, status=status.HTTP_400_BAD_REQUEST)

        option, created = InvestmentOption.objects.get_or_create(name=name,
                                                                 available_investment_id=available_investment)
        option.status = status
        if durations:
            option.duration.clear()
            for duration in durations:
                option.duration.add(duration)
        option.save()

        data = InvestmentOptionSerializer(option).data
        return Response(data)

    def put(self, request, pk):
        durations = request.data.get('duration')

        try:
            option = get_object_or_404(InvestmentOption, id=pk)
            option.name = request.data.get('name')
            option.status = request.data.get('status')
            option.available_investment_id = request.data.get('available_investment')
            if durations:
                option.duration.clear()
                for duration in durations:
                    option.duration.add(duration)
            option.save()
            data = InvestmentOptionSerializer(option).data
            return Response(data)
        except Exception as ex:
            return Response({'detail': str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            option = get_object_or_404(InvestmentOption, id=pk)
            option.delete()
        except Exception as ex:
            return Response({'detail': str(ex)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Investment Option deleted successfully'})


class AdminSavingsTypeView(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = SavingsTypeSerializer
    queryset = SavingsType.objects.all()
    lookup_field = 'id'


class AdminWalletView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_class = WalletFilter
    search_fields = ['user__user__first_name', 'user__user__last_name']


class AdminWalletDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    lookup_field = 'id'


class AdminLoanDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    lookup_field = 'id'


class AdminLoanView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = LoanSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_class = LoanFilter
    search_fields = ['user__user__first_name', 'user__user__last_name', 'user__user__email']
    queryset = Loan.objects.all().order_by('-id')


class AdminInvestmentView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = InvestmentSerializer
    queryset = Investment.objects.all().order_by('-id')
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filter_class = InvestmentFilter
    search_fields = ['name', 'type__name', 'description']
    lookup_field = 'id'


class AdminSavingView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = SavingSerializer
    queryset = Saving.objects.all().order_by('-id')
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['user__user__first_name', 'user__user__last_name', 'user__user__email']
    filter_class = SavingFilter
    lookup_field = 'id'


class AdminUserFilterView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserDetailSerializer
    queryset = Profile.objects.all().order_by('-id')
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filter_class = ProfileFilter
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'phone_number', 'member_id']






