from account.serializers import *
from loan.serializers import *
from savings.serializers import *
from investment.serializers import *
from settings.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser


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
    permission_classes = []
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


class AdminProfileView(ModelViewSet):
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


