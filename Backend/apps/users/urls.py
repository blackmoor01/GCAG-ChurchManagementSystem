from django.urls import path
from apps.users.views.authentication import (
    UserRegistrationView,
    CustomTokenObtainPairView,
    UserLogoutView,
    RefreshTokenView,
    UserProfileView,
    UserDetailView,
    ChangePasswordView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    VerifyEmailView,
    ResendVerificationEmailView,
    UserListView,
    UserActivationView,

)

urlpatterns = [
    # Authentication
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('token/refresh/', RefreshTokenView.as_view(), name='token-refresh'),
    
    # Profile Management
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),
    
    # Password Management
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    
    # Email Verification
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('resend-verification/', ResendVerificationEmailView.as_view(), name='resend-verification'),
    
    # Admin Operations
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:user_id>/activation/', UserActivationView.as_view(), name='user-activation'),
]