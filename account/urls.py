from django.urls import path
from .views import *


urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('membership/', PayMembershipFeeView.as_view(), name='membership'),
    path('faq/', FaqView.as_view(), name='faq'),
    path('feedback/', FeedbackMessageView.as_view(), name='feedback'),
    path('feedback/<int:id>/', FeedbackMessageDetailView.as_view(), name='feedback-detail'),
    path('user-detail/', UserDetailView.as_view(), name='user-detail'),
    path('add-guarantor/', AddGuarantorView.as_view(), name='add-guarantor'),
    path('update-guarantor/', UpdateGuarantorView.as_view(), name='update-guarantor'),
]
