from django.urls import path
from . import views

app_name = 'loan'
urlpatterns = [
    path('', views.LoanView.as_view(), name='loan'),
    path('<int:pk>/', views.LoanView.as_view(), name='loan-detail'),
    path('apply/', views.ApplyForLoanView.as_view(), name='apply'),
    path('duration/', views.LoanDurationView.as_view(), name='duration'),
    path('repay/', views.RepayLoanView.as_view(), name='repay'),
    path('verify-payment/', views.VerifyLoanPaymentView.as_view(), name='verify-payment'),
]

