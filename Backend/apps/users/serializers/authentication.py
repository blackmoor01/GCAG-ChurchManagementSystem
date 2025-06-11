from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from apps.users.models import User
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.password_validation import validate_password
from apps.users.utils.ip_utils import get_client_ip

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'password2', 
                  'phone_number', 'date_of_birth', 'gender', 'address', 'baptized')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data.pop('password2')
        
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data.get('phone_number', ''),
            date_of_birth=validated_data.get('date_of_birth'),
            gender=validated_data.get('gender'),
            address=validated_data.get('address'),
        )
        
        # Track registration IP
        if request:
            ip = get_client_ip(request)
            if ip:
                user.registration_ip_address = ip
                user.save()
        
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        request = self.context.get('request')
        
        authenticate_kwargs = {
            'email': attrs.get(self.username_field),
            'password': attrs.get('password'),
        }
        
        try:
            authenticate_kwargs['request'] = request
        except KeyError:
            pass
        
        self.user = authenticate(**authenticate_kwargs)
        
        if self.user is None:
            raise AuthenticationFailed(
                _('No active account found with the given credentials'),
                code='authentication_failed',
            )
            
        if not self.user.is_active:
            raise AuthenticationFailed(
                _('Account is not active'),
                code='account_inactive',
            )
            
        # Track login IP
        if request:
            ip = get_client_ip(request)
            if ip:
                self.user.last_login_ip = ip
                self.user.login_ip_address = ip
                self.user.save()
        
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'role': self.user.role,
            'is_email_verified': self.user.is_email_verified,
            'mfa_enabled': self.user.mfa_enabled,
        }
        
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'phone_number', 
                  'role', 'member_id', 'ministry', 'membership_start_date', 
                  'baptized', 'date_of_birth', 'gender', 'address', 
                  'is_email_verified', 'mfa_enabled')
        read_only_fields = ('id', 'email', 'role', 'member_id', 'membership_start_date')

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs

class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)