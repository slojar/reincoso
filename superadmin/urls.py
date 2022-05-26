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
    path('user-investment/', AdminUserInvestmentView.as_view(), name='user-investment'),
    path('user-investment/<int:id>/', AdminUserInvestmentDetailView.as_view(), name='user-investment-detail'),
    path('user-filter/', AdminUserFilterView.as_view(), name='user-filter'),
    path('group/', AdminGroupView.as_view(), name='group'),
    path('activity/', AdminActivityLog.as_view(), name='activity'),
    path('activity/<int:id>/', AdminActivityLogDetail.as_view(), name='activity-detail'),
    path('update-banks/', UpdateBankView.as_view(), name='update-banks'),

    path('notification/', AdminNotificationView.as_view(), name='admin-notification'),
    path('notification/<int:notification_id>/', AdminNotificationView.as_view(), name='admin-notification-detail'),

    path('withdrawal/', AdminWithdrawalView.as_view(), name='admin-withdrawal'),
    path('withdrawal/<int:withdrawal_id>/', AdminWithdrawalView.as_view(), name='admin-withdrawal-detail'),


    # path('transfer/', TransferFundView.as_view(), name='transfer-fund'),
    # path('transfer/<str:transaction_ref>/', TransferFundView.as_view(), name='transfer-fund'),
]

urlpatterns += router.urls

