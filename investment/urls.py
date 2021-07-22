from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.InvestmentsView.as_view()),
    path('apply/', views.InvestView.as_view()),
]
