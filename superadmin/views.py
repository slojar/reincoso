from account.serializers import *
from loan.serializers import *
from savings.serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser


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


class AdminProfileView(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = UserDetailSerializer
    queryset = Profile.objects.all()
    lookup_field = 'id'


class AdminLoanDurationView(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = LoanDurationSerializer
    queryset = LoanDuration
    lookup_field = 'id'


class AdminLoanTransactionView(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = LoanTransactionSerializer
    queryset = LoanTransaction.objects.all()
    lookup_field = 'id'


class AdminLoanView(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = LoanSerializer
    queryset = Loan.objects.all()
    lookup_field = 'id'


class AdminSavingDuration(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = SavingDurationSerializer
    queryset = Duration.objects.all()
    lookup_field = 'id'


class AdminSavingTransaction(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = SavingTransactionSerializer
    queryset = SavingTransaction.objects.all()
    lookup_field = 'id'


class AdminSavingsSerializer(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = SavingSerializer
    queryset = Saving.objects.all()
    lookup_field = 'id'


