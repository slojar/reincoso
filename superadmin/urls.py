from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()

router.register('faq', AdminFaqView)
router.register('faq-category', AdminFaqCategoryView)
router.register('feedbacks', AdminFeedbackMessageView)
router.register('users', AdminProfileView)
router.register('loan-duration', AdminLoanDurationView)
router.register('loan-transaction', AdminLoanTransactionView)
router.register('saving-duration', AdminSavingDurationView)
router.register('saving-transaction', AdminSavingTransactionView)
router.register('investment-option', AdminInvestmentOptionView)
router.register('investment-specifiication', AdminInvestmentSpecificationView)
router.register('general-setting', AdminGeneralSettingView)
router.register('payment-gateway', AdminPaymentGatewayView)
router.register('loan-setting', AdminLoanSettingView)

urlpatterns = [
    path('', AdminHomepage.as_view(), name='homepage'),
]

urlpatterns += router.urls

