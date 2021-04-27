from django.urls import path
from savings.views import SavingsView
from .views import *


urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('membership/', PayMembershipView.as_view(), name='membership'),
    path('faq/', FaqView.as_view(), name='faq'),
    path('feedback/', FeedbackMessageView.as_view(), name='feedback'),
    path('feedback/<int:id>/', FeedbackMessageDetailView.as_view(), name='feedback-detail'),
    path('saving/', SavingsView.as_view(), name='saving'),
]
