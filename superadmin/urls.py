from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()

router.register('faq', AdminFaqView)
router.register('faq-category', AdminFaqCategoryView)
router.register('feedbacks', AdminFeedbackMessageView)
# router.register('users', AdminProfileView)
router.register('loan-duration', AdminLoanDurationView)
router.register('loan-transaction', AdminLoanTransactionView)
router.register('saving-duration', AdminSavingDurationView)
router.register('saving-transaction', AdminSavingTransactionView)
router.register('available-investment', AdminAvailableInvestmentView)
# router.register('investment-option', AdminInvestmentOptionView)
router.register('investment-duration', AdminInvestmentDurationView)
router.register('investment-specifiication', AdminInvestmentSpecificationView)
router.register('general-setting', AdminGeneralSettingView)
router.register('payment-gateway', AdminPaymentGatewayView)
router.register('loan-setting', AdminLoanSettingView)
router.register('saving-type', AdminSavingsTypeView)

urlpatterns = [
    path('', AdminHomepage.as_view(), name='homepage'),
    path('users/', AdminProfileView.as_view(), name='user'),
    path('users/<int:profile_id>/', AdminProfileView.as_view(), name='user-detail'),
    path('site/', AdminSiteView.as_view(), name='site'),
    path('investment-option/', AdminInvestmentOptionView.as_view(), name='investment-option'),
    path('investment-option/<int:pk>/', AdminInvestmentOptionView.as_view(), name='investment-option-detail'),
    path('wallet/', AdminWalletView.as_view(), name='user-wallet'),
    path('wallet/<int:id>/', AdminWalletDetailView.as_view(), name='user-wallet-detail'),
    path('loan/', AdminLoanView.as_view(), name='loan'),
    path('loan/<int:id>/', AdminLoanDetailView.as_view(), name='loan-detail'),
    path('saving/', AdminSavingView.as_view(), name='saving'),
    path('saving/<int:id>/', AdminSavingView.as_view(), name='saving-detail'),
    path('investment/', AdminInvestmentView.as_view(), name='investment'),
    path('investment/<int:id>/', AdminInvestmentView.as_view(), name='investment-detail'),
]

urlpatterns += router.urls

