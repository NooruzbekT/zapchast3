from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserProfileView, EmailVerificationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('verify-email/', EmailVerificationView.as_view(), name='verify-email'),
]