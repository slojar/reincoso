from django.urls import path
from .views import *


urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('faq/', FaqView.as_view(), name='faq'),
    path('feedback/', FeedbackMessageView.as_view(), name='feedback'),
    path('feedback/<int:id>/', FeedbackMessageDetailView.as_view(), name='feedback-detail'),
]
