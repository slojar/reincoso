from django.urls import path
from . import views


urlpatterns = [
    path('apply/', views.ApplyForLoanView().as_view(), )
]

