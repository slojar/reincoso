from django.urls import path
from .views import *

app_name = 'savings'
urlpatterns = [
    path('', SavingsView.as_view(), name='saving'),
    path('verify-payment/', VerifyPaymentView.as_view(), name='verify-payment'),
]
