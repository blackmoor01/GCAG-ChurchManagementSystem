from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from apps.users.utils.ip_utils import get_client_ip
from apps.users.models import User

from apps.users.serializers.authentication import (
    UserRegistrationSerializer,
    CustomTokenObtainPairSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
    EmailVerificationSerializer,
)
from apps.users.services.auth_service import AuthService

class UserRegistrationView(APIView):
    """
    Handle user registration
    POST: Create new user account
    """
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            
            # Send verification email
            AuthService.send_verification_email(user, request)
            
            return Response({
                'message': 'User registered successfully. Please check your email for verification.',
                'user': UserProfileSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Handle user login
    POST: Authenticate user and return JWT tokens
    """
    serializer_class = CustomTokenObtainPairSerializer

class UserLogoutView(APIView):
    """
    Handle user logout
    POST: Blacklist refresh token and logout user
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            logout(request)
            return Response({"message": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    """
    Handle user profile operations
    GET: Retrieve user profile
    PUT: Update entire user profile
    PATCH: Partially update user profile
    DELETE: Deactivate/delete user account
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get current user's profile"""
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        """Update entire user profile"""
        serializer = UserProfileSerializer(request.user, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profile updated successfully.',
                'data': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """Partially update user profile"""
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profile updated successfully.',
                'data': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """Deactivate user account (soft delete)"""
        user = request.user
        
        # Soft delete - deactivate account instead of hard delete
        user.is_active = False
        user.save()
        
        try:
            # Get all refresh tokens for this user and blacklist them
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except Exception:
            pass  # Continue with account deactivation even if token blacklisting fails
        
        logout(request)
        return Response({
            'message': 'Account deactivated successfully.'
        }, status=status.HTTP_204_NO_CONTENT)

class UserDetailView(APIView):
    """
    Handle operations on specific users (admin functionality)
    GET: Retrieve specific user profile
    PUT: Update entire user profile (admin only)
    PATCH: Partially update user profile (admin only)
    DELETE: Deactivate/delete specific user account (admin only)
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, user_id):
        """Helper method to get user object"""
        return get_object_or_404(User, id=user_id)

    def get(self, request, user_id):
        """Get specific user's profile"""
        # Check if user is accessing their own profile or is admin
        if request.user.id != user_id and not request.user.is_staff:
            return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        
        user = self.get_object(user_id)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def put(self, request, user_id):
        """Update entire user profile (admin only)"""
        if not request.user.is_staff:
            return Response({"error": "Admin permission required."}, status=status.HTTP_403_FORBIDDEN)
        
        user = self.get_object(user_id)
        serializer = UserProfileSerializer(user, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'User profile updated successfully.',
                'data': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, user_id):
        """Partially update user profile (admin only)"""
        if not request.user.is_staff:
            return Response({"error": "Admin permission required."}, status=status.HTTP_403_FORBIDDEN)
        
        user = self.get_object(user_id)
        serializer = UserProfileSerializer(user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'User profile updated successfully.',
                'data': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        """Deactivate specific user account (admin only)"""
        if not request.user.is_staff:
            return Response({"error": "Admin permission required."}, status=status.HTTP_403_FORBIDDEN)
        
        user = self.get_object(user_id)
        user.is_active = False
        user.save()
        
        return Response({
            'message': f'User account {user.email} deactivated successfully.'
        }, status=status.HTTP_204_NO_CONTENT)

class ChangePasswordView(APIView):
    """
    Handle password change
    POST: Change user password
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({"old_password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            # Optionally logout user from all devices after password change
            # This would require blacklisting all existing tokens
            
            return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    """
    Handle email verification
    POST: Verify email with token
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            user = AuthService.verify_email_token(
                serializer.validated_data['uid'],
                serializer.validated_data['token']
            )
            if user:
                return Response({"message": "Email successfully verified."}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid verification link."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResendVerificationEmailView(APIView):
    """
    Handle resending verification email
    POST: Resend verification email
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.is_email_verified:
            return Response({"message": "Email is already verified."}, status=status.HTTP_400_BAD_REQUEST)
        
        success = AuthService.send_verification_email(request.user, request)
        if success:
            return Response({"message": "Verification email resent."}, status=status.HTTP_200_OK)
        return Response({"error": "Failed to send verification email."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PasswordResetRequestView(APIView):
    """
    Handle password reset request
    POST: Send password reset email
    """
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
            success = AuthService.send_password_reset_email(user, request)
            if success:
                return Response({"message": "Password reset link sent to your email."}, status=status.HTTP_200_OK)
            return Response({"error": "Failed to send password reset email."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except User.DoesNotExist:
            # Return success message even if user doesn't exist for security reasons
            # This prevents email enumeration attacks
            return Response({"message": "If an account with this email exists, a password reset link has been sent."}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(APIView):
    """
    Handle password reset confirmation
    POST: Reset password with token
    """
    permission_classes = [AllowAny]

    def post(self, request):
        uid = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        
        if not all([uid, token, new_password]):
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = AuthService.validate_password_reset_token(uid, token)
        if user:
            user.set_password(new_password)
            user.save()
            
            # Optionally blacklist all existing tokens for security
            # This would force re-login on all devices
            
            return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid reset link."}, status=status.HTTP_400_BAD_REQUEST)

class RefreshTokenView(APIView):
    """
    Handle token refresh
    POST: Refresh access token using refresh token
    """
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = RefreshToken(refresh_token)
            access_token = str(token.access_token)
            
            return Response({
                'access': access_token,
                'message': 'Token refreshed successfully.'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid refresh token."}, status=status.HTTP_401_UNAUTHORIZED)

class UserListView(APIView):
    """
    Handle user list operations (admin only)
    GET: List all users
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get list of all users (admin only)"""
        if not request.user.is_staff:
            return Response({"error": "Admin permission required."}, status=status.HTTP_403_FORBIDDEN)
        
        users = User.objects.all()
        serializer = UserProfileSerializer(users, many=True)
        return Response({
            'count': users.count(),
            'users': serializer.data
        })

class UserActivationView(APIView):
    """
    Handle user account activation/deactivation (admin only)
    PATCH: Activate or deactivate user account
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, user_id):
        """Activate or deactivate user account"""
        if not request.user.is_staff:
            return Response({"error": "Admin permission required."}, status=status.HTTP_403_FORBIDDEN)
        
        user = get_object_or_404(User, id=user_id)
        is_active = request.data.get('is_active')
        
        if is_active is None:
            return Response({"error": "is_active field is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        user.is_active = bool(is_active)
        user.save()
        
        action = "activated" if user.is_active else "deactivated"
        return Response({
            'message': f'User account {user.email} {action} successfully.',
            'user': UserProfileSerializer(user).data
        })