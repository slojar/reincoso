from django.urls import path
from .views import *

urlpatterns = [
    path('', SavingsView.as_view(), name='saving'),
    path('duration/', SavingDurationView.as_view(), name='duration'),

]
