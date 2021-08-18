from django.urls import path
from .views import *

app_name = 'savings'
urlpatterns = [
    path('', SavingsView.as_view(), name='saving'),
    path('my-savings/', MySavingsView.as_view(), name='my-savings'),
    path('my-savings/<int:pk>/', MySavingsDetailView.as_view(), name='my-savings-detail'),
    path('my-savings/<int:savings_id>/transactions/', SavingTransactionView.as_view(), name='savings-transaction'),
    path('transaction/<int:pk>/', SavingTransactionDetailView.as_view(), name='savings-transaction-detail'),
    path('verify-payment/', VerifyPaymentView.as_view(), name='verify-payment'),
]

