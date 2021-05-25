from django.urls import path
from . import views


urlpatterns = [
    path('apply/', views.ApplyForLoanView().as_view(), name='apply'),
    path('duration/', views.LoanDurationView().as_view(), name='duration'),
]

