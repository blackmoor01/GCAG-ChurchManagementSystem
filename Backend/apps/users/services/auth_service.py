from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from apps.users.models import User
import logging

logger = logging.getLogger(__name__)

class AuthService:
    @staticmethod
    def send_verification_email(user, request):
        try:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            verification_link = f"{settings.FRONTEND_URL}/verify-email/{uid}/{token}/"
            
            subject = "Verify Your Email Address"
            message = render_to_string('users/email/verification_email.html', {
                'user': user,
                'verification_link': verification_link,
            })
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
                html_message=message
            )
            return True
        except Exception as e:
            logger.error(f"Error sending verification email: {e}")
            return False

    @staticmethod
    def verify_email_token(uidb64, token):
        try:
            user = User.objects.get(pk=urlsafe_base64_decode(uidb64).decode())
            if default_token_generator.check_token(user, token):
                user.is_email_verified = True
                user.save()
                return user
            return None
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return None

    @staticmethod
    def send_password_reset_email(user, request):
        try:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
            
            subject = "Password Reset Request"
            message = render_to_string('users/email/password_reset_email.html', {
                'user': user,
                'reset_link': reset_link,
            })
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
                html_message=message
            )
            return True
        except Exception as e:
            logger.error(f"Error sending password reset email: {e}")
            return False

    @staticmethod
    def validate_password_reset_token(uidb64, token):
        try:
            user = User.objects.get(pk=urlsafe_base64_decode(uidb64).decode())
            if default_token_generator.check_token(user, token):
                return user
            return None
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return None