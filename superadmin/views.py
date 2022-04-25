from decimal import Decimal

from account.serializers import *
from account.utils import signup, reformat_phone_number, decrypt_text
from loan.serializers import *
from loan.paginations import CustomPagination
from savings.serializers import *
from investment.serializers import *
from settings.serializers import *
from .filters import *
from .models import Transfer
from .serializers import TransferSerializer
from .permissions import *
from .utils import *
from account.utils import encrypt_text
from modules.paystack import get_banks, initialize_transfer, finalize_transfer
from threading import Thread

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser

from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import ActivityReportSerializer


class AdminHomepage(APIView):

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
    serializer_class = FaqSerializer
    pagination_class = CustomPagination
    queryset = Faq.objects.all()
    lookup_field = 'id'
    model = 'Faq'

    def list(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not can_change(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        model_id = 0
        for i in self.get_queryset():
            model_id = i.id
        create_log(request, model=eval(self.model.strip('')), model_id=model_id)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not can_delete(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        model_id = 0
        for i in self.get_queryset():
            model_id = i.id
        create_log(request, model=eval(self.model.strip('')), model_id=model_id)
        return super().destroy(request, *args, **kwargs)


class AdminFaqCategoryView(ModelViewSet):
    pagination_class = CustomPagination
    serializer_class = FaqCategorySerializer
    queryset = FaqCategory.objects.all()
    lookup_field = 'id'
    model = 'FaqCategory'

    def list(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not can_change(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        model_id = 0
        for i in self.get_queryset():
            model_id = i.id
        create_log(request, model=eval(self.model.strip('')), model_id=model_id)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not can_delete(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        model_id = 0
        for i in self.get_queryset():
            model_id = i.id
        create_log(request, model=eval(self.model.strip('')), model_id=model_id)
        return super().destroy(request, *args, **kwargs)


class AdminFeedbackMessageView(ModelViewSet):
    pagination_class = CustomPagination
    serializer_class = FeedbackMessageSerializer
    queryset = FeedbackMessage.objects.all()
    lookup_field = 'id'
    model = 'FeedbackMessage'

    def list(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not can_change(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        model_id = 0
        for i in self.get_queryset():
            model_id = i.id
        create_log(request, model=eval(self.model.strip('')), model_id=model_id)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not can_delete(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        model_id = 0
        for i in self.get_queryset():
            model_id = i.id
        create_log(request, model=eval(self.model.strip('')), model_id=model_id)
        return super().destroy(request, *args, **kwargs)


# class AdminProfileViewOld(ModelViewSet):
#     permission_classes = [IsAdminUser]
#     serializer_class = UserDetailSerializer
#     queryset = Profile.objects.all()
#     lookup_field = 'id'


class AdminLoanDurationView(ModelViewSet):
    pagination_class = CustomPagination
    serializer_class = LoanDurationSerializer
    queryset = LoanDuration.objects.all()
    lookup_field = 'id'
    model = 'LoanDuration'

    def list(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not can_change(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        model_id = 0
        for i in self.get_queryset():
            model_id = i.id
        create_log(request, model=eval(self.model.strip('')), model_id=model_id)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not can_delete(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        model_id = 0
        for i in self.get_queryset():
            model_id = i.id
        create_log(request, model=eval(self.model.strip('')), model_id=model_id)
        return super().destroy(request, *args, **kwargs)


class AdminLoanTransactionView(ModelViewSet):
    pagination_class = CustomPagination
    serializer_class = LoanTransactionSerializer
    queryset = LoanTransaction.objects.all()
    lookup_field = 'id'
    model = 'LoanTransaction'

    def list(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not can_change(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        model_id = 0
        for i in self.get_queryset():
            model_id = i.id
        create_log(request, model=eval(self.model.strip('')), model_id=model_id)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not can_delete(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        model_id = 0
        for i in self.get_queryset():
            model_id = i.id
        create_log(request, model=eval(self.model.strip('')), model_id=model_id)
        return super().destroy(request, *args, **kwargs)


class AdminSavingDurationView(ModelViewSet):
    pagination_class = CustomPagination
    serializer_class = SavingDurationSerializer
    queryset = Duration.objects.all()
    lookup_field = 'id'
    model = 'Duration'

    def list(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not can_change(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        model_id = 0
        for i in self.get_queryset():
            model_id = i.id
        create_log(request, model=eval(self.model.strip('')), model_id=model_id)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not can_delete(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        model_id = 0
        for i in self.get_queryset():
            model_id = i.id
        create_log(request, model=eval(self.model.strip('')), model_id=model_id)
        return super().destroy(request, *args, **kwargs)


class AdminSavingTransactionView(ModelViewSet):
    pagination_class = CustomPagination
    queryset = SavingTransaction.objects.all()
    serializer_class = SavingTransactionSerializer
    lookup_field = 'id'
    model = 'SavingTransaction'

    def list(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not can_change(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        model_id = 0
        for i in self.get_queryset():
            model_id = i.id
        create_log(request, model=eval(self.model.strip('')), model_id=model_id)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not can_delete(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        model_id = 0
        for i in self.get_queryset():
            model_id = i.id
        create_log(request, model=eval(self.model.strip('')), model_id=model_id)
        return super().destroy(request, *args, **kwargs)


class AdminInvestmentSpecificationView(ModelViewSet):
    queryset = InvestmentSpecification.objects.all()
    serializer_class = InvestmentSpecificationSerializer
    pagination_class = CustomPagination
    lookup_field = 'id'
    model = 'InvestmentSpecification'

    def list(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not can_change(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        model_id = 0
        for i in self.get_queryset():
            model_id = i.id
        create_log(request, model=eval(self.model.strip('')), model_id=model_id)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not can_delete(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        model_id = 0
        for i in self.get_queryset():
            model_id = i.id
        create_log(request, model=eval(self.model.strip('')), model_id=model_id)
        return super().destroy(request, *args, **kwargs)


class AdminGeneralSettingView(ModelViewSet):
    serializer_class = GeneralSettingsSerializer
    pagination_class = CustomPagination
    queryset = GeneralSettings.objects.all()
    lookup_field = 'id'
    model = 'GeneralSettings'

    def list(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not can_change(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        model_id = 0
        for i in self.get_queryset():
            model_id = i.id
        create_log(request, model=eval(self.model.strip('')), model_id=model_id)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not can_delete(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        model_id = 0
        for i in self.get_queryset():
            model_id = i.id
        create_log(request, model=eval(self.model.strip('')), model_id=model_id)
        return super().destroy(request, *args, **kwargs)


class AdminPaymentGatewayView(ModelViewSet):
    model = 'PaymentGateway'
    pagination_class = CustomPagination
    serializer_class = PaymentGatewaySerializer
    queryset = PaymentGateway.objects.all()
    lookup_field = 'id'

    def list(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not can_change(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        model_id = 0
        for i in self.get_queryset():
            model_id = i.id
        create_log(request, model=eval(self.model.strip('')), model_id=model_id)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not can_delete(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        model_id = 0
        for i in self.get_queryset():
            model_id = i.id
        create_log(request, model=eval(self.model.strip('')), model_id=model_id)
        return super().destroy(request, *args, **kwargs)


class AdminLoanSettingView(ModelViewSet):
    pagination_class = CustomPagination
    serializer_class = LoanSettingSerializer
    queryset = LoanSetting.objects.all()
    model = 'LoanSetting'
    lookup_field = 'id'

    def list(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not can_change(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        model_id = 0
        for i in self.get_queryset():
            model_id = i.id
        create_log(request, model=eval(self.model.strip('')), model_id=model_id)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not can_delete(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        model_id = 0
        for i in self.get_queryset():
            model_id = i.id
        create_log(request, model=eval(self.model.strip('')), model_id=model_id)
        return super().destroy(request, *args, **kwargs)


class AdminSiteView(generics.ListAPIView):
    pagination_class = CustomPagination
    serializer_class = SiteSerializer
    queryset = Site.objects.all()
    model = Site

    def list(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().list(request, *args, **kwargs)


class AdminInvestmentDurationView(ModelViewSet):
    pagination_class = CustomPagination
    serializer_class = InvestmentDurationSerializer
    queryset = InvestmentDuration.objects.all()
    lookup_field = 'id'
    model = 'InvestmentDuration'

    def list(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not can_change(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        model_id = 0
        for i in self.get_queryset():
            model_id = i.id
        create_log(request, model=eval(self.model.strip('')), model_id=model_id)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not can_delete(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        model_id = 0
        for i in self.get_queryset():
            model_id = i.id
        create_log(request, model=eval(self.model.strip('')), model_id=model_id)
        return super().destroy(request, *args, **kwargs)


class AdminAvailableInvestmentView(ModelViewSet):
    pagination_class = CustomPagination
    serializer_class = InvestmentSerializer
    queryset = Investment.objects.all()
    lookup_field = 'id'
    model = 'Investment'

    def list(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not can_change(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        model_id = 0
        for i in self.get_queryset():
            model_id = i.id
        create_log(request, model=eval(self.model.strip('')), model_id=model_id)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not can_delete(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        model_id = 0
        for i in self.get_queryset():
            model_id = i.id
        create_log(request, model=eval(self.model.strip('')), model_id=model_id)
        return super().destroy(request, *args, **kwargs)


class AdminProfileView(APIView, CustomPagination):
    model = 'User'

    def get(self, request, profile_id=None):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)

        if profile_id:
            user = Profile.objects.get(id=profile_id)
            serializer = UserDetailSerializer(user).data
        else:
            user = Profile.objects.all().order_by('-id')
            user = self.paginate_queryset(user, request)
            user = UserDetailSerializer(user, many=True).data
            serializer = self.get_paginated_response(user).data
        return Response(serializer)

    def put(self, request, profile_id):
        # if not can_change(request.user, self.model):
        #     return Response({'detail': 'You do not have permission to perform this action'})
        if request.user.is_staff is False:
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            phone_number = request.data.get('phone_number')
            group_name = request.data.get('group_name')

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
            if not group_name:
                profile.user.groups.clear()
            if group_name:
                for name in group_name:
                    group = Group.objects.get(name__exact=name)
                    profile.user.groups.add(group)

            profile.user.save()
            profile.save()
            data = UserDetailSerializer(profile).data
            create_log(request, model=eval(self.model.strip('')), model_id=profile.user.id)
            return Response(data)
        except Exception as ex:
            return Response({'detail': str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, profile_id):
        if not can_delete(request.user, self.model) or not can_delete(request.user, 'profile'):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            profile = get_object_or_404(Profile, id=profile_id)
            model_id = profile.user.id
            profile.delete()
            create_log(request, model=eval(self.model.strip('')), model_id=model_id)
            return Response({'detail': 'profile deleted successfully'})
        except Exception as ex:
            return Response({'detail': str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class AdminInvestmentOptionView(APIView, CustomPagination):
    model = 'InvestmentOption'

    def get(self, request, pk=None):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
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
        if not can_add(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)

        name = request.data.get('name')
        option_status = request.data.get('status')
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
        option.status = option_status
        if durations:
            option.duration.clear()
            for duration in durations:
                option.duration.add(duration)
        option.save()

        data = InvestmentOptionSerializer(option).data
        create_log(request, model=eval(self.model.strip('')), model_id=option.id)
        return Response(data)

    def put(self, request, pk):
        if not can_change(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)

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
            create_log(request, model=eval(self.model.strip('')), model_id=option.id)
            return Response(data)
        except Exception as ex:
            return Response({'detail': str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not can_delete(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            option = get_object_or_404(InvestmentOption, id=pk)
            model_id = option.id
            option.delete()
            create_log(request, model=eval(self.model.strip('')), model_id=model_id)
        except Exception as ex:
            return Response({'detail': str(ex)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Investment Option deleted successfully'})


class AdminSavingsTypeView(ModelViewSet):
    pagination_class = CustomPagination
    serializer_class = SavingsTypeSerializer
    queryset = SavingsType.objects.all()
    lookup_field = 'id'
    model = 'SavingsType'

    def list(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not can_change(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        model_id = 0
        for i in self.get_queryset():
            model_id = i.id
        create_log(request, model=eval(self.model.strip('')), model_id=model_id)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not can_delete(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        model_id = 0
        for i in self.get_queryset():
            model_id = i.id
        create_log(request, model=eval(self.model.strip('')), model_id=model_id)
        return super().destroy(request, *args, **kwargs)


class AdminWalletView(generics.ListAPIView):
    pagination_class = CustomPagination
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_class = WalletFilter
    search_fields = ['user__user__first_name', 'user__user__last_name']
    model = 'Wallet'

    def list(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().list(request, *args, **kwargs)


class AdminWalletDetailView(generics.RetrieveUpdateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    lookup_field = 'id'
    model = 'Wallet'

    def retrieve(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not can_change(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        model_id = 0
        for i in self.get_queryset():
            model_id = i.id
        create_log(request, model=eval(self.model.strip('')), model_id=model_id)
        return super().update(request, *args, **kwargs)


class AdminLoanDetailView(generics.RetrieveUpdateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    lookup_field = 'id'
    model = 'Loan'

    def retrieve(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not can_change(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        model_id = 0
        for i in self.get_queryset():
            model_id = i.id
        create_log(request, model=eval(self.model.strip('')), model_id=model_id)
        return super().update(request, *args, **kwargs)


class AdminLoanView(generics.ListAPIView):
    pagination_class = CustomPagination
    serializer_class = LoanSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_class = LoanFilter
    search_fields = ['user__user__first_name', 'user__user__last_name', 'user__user__email']
    queryset = Loan.objects.all().order_by('-id')
    model = 'Loan'

    def list(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().list(request, *args, **kwargs)


class AdminInvestmentView(generics.ListAPIView):
    pagination_class = CustomPagination
    serializer_class = InvestmentSerializer
    queryset = Investment.objects.all().order_by('-id')
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filter_class = InvestmentFilter
    search_fields = ['name', 'type__name', 'description']
    lookup_field = 'id'
    model = 'Investment'

    def list(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().list(request, *args, **kwargs)


class AdminUserInvestmentView(generics.ListAPIView):
    pagination_class = CustomPagination
    serializer_class = UserInvestmentSerializer
    queryset = UserInvestment.objects.all().order_by('-id')
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filter_class = UserInvestmentFilter
    search_fields = ['user__user__first_name', 'user__user__last_name', 'user__user__email', 'investment__name']
    lookup_field = 'id'
    model = 'UserInvestment'

    def list(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().list(request, *args, **kwargs)


class AdminSavingView(generics.ListAPIView):
    pagination_class = CustomPagination
    serializer_class = SavingSerializer
    queryset = Saving.objects.all().order_by('-updated_on')
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['user__user__first_name', 'user__user__last_name', 'user__user__email']
    filter_class = SavingFilter
    lookup_field = 'id'
    model = 'Saving'

    def list(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().list(request, *args, **kwargs)


class AdminUserFilterView(generics.ListAPIView):
    pagination_class = CustomPagination
    serializer_class = UserDetailSerializer
    queryset = Profile.objects.all().order_by('-id')
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filter_class = ProfileFilter
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'phone_number', 'member_id']
    model = 'Profile'

    def list(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().list(request, *args, **kwargs)


class AdminGroupView(generics.ListAPIView):
    pagination_class = CustomPagination
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    model = 'Group'

    def list(self, request, *args, **kwargs):
        if not can_view(request.user, self.model):
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().list(request, *args, **kwargs)


class AdminActivityLog(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination
    queryset = LogEntry.objects.all().order_by('-id')
    serializer_class = ActivityReportSerializer
    lookup_field = 'id'


class AdminActivityLogDetail(generics.RetrieveAPIView):
    permission_classes = [IsAdminUser]
    queryset = LogEntry.objects.all()
    serializer_class = ActivityReportSerializer
    lookup_field = 'id'


class UpdateBankView(APIView):
    permission_classes = []

    def get(self, request):
        Thread(target=get_banks, args=[]).start()
        return Response({"detail": "Banks updated"})


class TransferFundView(APIView, CustomPagination):
    permission_classes = [IsAdminUser]

    def get(self, request):
        transfer = self.paginate_queryset(Transfer.objects.all().order_by('-id'), request)
        transfer = TransferSerializer(transfer, many=True).data
        result = self.get_paginated_response(transfer).data
        return Response(result)

    def post(self, request):
        user = request.data.get('profile_id')
        description = request.data.get('description')
        amount = request.data.get('amount')

        if not (user and amount):
            return Response({"detail": "profile_id and amount are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            profile = Profile.objects.get(id=user)
            recipient_code = profile.recipient_code

            paystack_amount = amount * 100

            response = initialize_transfer(recipient_code, description, paystack_amount)

            if response['status'] is True:
                transfer_code = response['data']['transfer_code']
                transfer, _ = Transfer.objects.get_or_create(reference=transfer_code)
                transfer.recipient_name = profile.account_name
                transfer.recipient_account_no = profile.account_no
                transfer.amount = amount
                transfer.description = description
                transfer.created_by = request.user
                transfer.save()
                return Response({"detail": "Transfer added successfully", "data": TransferSerializer(transfer).data})
            else:
                return Response({"detail": response['message']}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": "An error has occurred", "error": f'{e}'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, transaction_ref):
        otp = request.data.get("otp")

        if not otp:
            return Response({'detail': 'OTP is required to approve transfer'}, status=status.HTTP_400_BAD_REQUEST)

        if not Transfer.objects.filter(reference=transaction_ref, status='pending').exists():
            return Response({'detail': 'Reference number not found or is approved'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            response = finalize_transfer(transaction_ref, otp)
            if response['status'] is True and response['data']['status'] == 'success':
                transfer = Transfer.objects.get(reference=transaction_ref)
                transfer.status = "successful"
                transfer.updated_by = request.user
                transfer.save()
                return Response({'detail': 'Transfer approved'})
            else:
                return Response({'detail': 'Transfer failed'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'detail': 'Transfer failed', 'error': f'{err}'}, status=status.HTTP_400_BAD_REQUEST)







