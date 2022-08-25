from django.contrib import admin
from django.urls import path
from . import views
# from .views import investment_maturity_cron_view, investment_yield_cron_view

urlpatterns = [
    path('investment-types/', views.InvestmentTypesView.as_view()),
    path('investment-types/<str:id>/', views.InvestmentTypesDetailView.as_view()),
    path('apply/', views.InvestView.as_view()),
    path('pay/', views.InvestPaymentView.as_view()),
    path('', views.InvestmentsView.as_view()),
    path('mine/', views.MyInvestmentView.as_view()),
    path('mine/<int:id>/', views.MyInvestmentDetailView.as_view()),

    path('options/', views.InvestmentOptionsView.as_view()),
    path('options/<str:id>/', views.InvestmentOptionDetailView.as_view()),

    path('<str:id>/', views.InvestmentDetailView.as_view()),
    path('<str:id>/options/', views.InvestmentOptionsView.as_view()),

    # CRONJOB
    path('maturity-check-cron', views.investment_maturity_cron_view),
    path('interest-cron/', views.investment_yield_cron_view),
]

