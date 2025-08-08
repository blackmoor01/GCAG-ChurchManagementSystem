import uuid
import random
import string
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Ministry(models.TextChoices):
    # Consolidated ministry choices used across the application
    PASTORAL = 'PASTORAL', 'Pastoral Care'
    WORSHIP = 'WORSHIP', 'Worship & Music'
    YOUTH = 'YOUTH', 'Youth Ministry'
    CHILDREN = 'CHILDREN', 'Children Ministry'
    EVANGELISM = 'EVANGELISM', 'Evangelism & Outreach'
    EDUCATION = 'EDUCATION', 'Christian Education'
    FELLOWSHIP = 'FELLOWSHIP', 'Fellowship & Community'
    MISSIONS = 'MISSIONS', 'Missions & Service'
    ADMINISTRATION = 'ADMIN', 'Administration'
    MEDIA = 'MEDIA', 'Media & Technology'
    CHOIR = 'CHOIR', 'Choir'
    USHERING = 'USHER', 'Ushering'
    FINANCE = 'FIN', 'Finance'
    PRAYER = 'PRAY', 'Prayer'
    WOMEN = 'WOMEN', 'Women'
    MEN = 'MEN', 'Men'
    YOUNG_SINGLES = 'YS', 'Young Singles'

class Role(models.TextChoices):
    ADMIN = 'ADMIN', 'Admin'
    MEMBER = 'MEMBER', 'Member'
    HEAD_PASTOR = 'HEAD_PASTOR', 'Head Pastor'

class Gender(models.TextChoices):
    # Standardized gender choices
    MALE = 'MALE', 'Male'
    FEMALE = 'FEMALE', 'Female'
    OTHER = 'OTHER', 'Other'

class MaritalStatus(models.TextChoices):
    # Standardized marital status choices
    SINGLE = 'SINGLE', 'Single'
    MARRIED = 'MARRIED', 'Married'
    DIVORCED = 'DIVORCED', 'Divorced'
    WIDOWED = 'WIDOWED', 'Widowed'
    SEPARATED = 'SEPARATED', 'Separated'

class MembershipStatus(models.TextChoices):
    # Standardized membership status choices
    ACTIVE = 'ACTIVE', 'Active'
    INACTIVE = 'INACTIVE', 'Inactive'
    TRANSFERRED = 'TRANSFERRED', 'Transferred'
    DECEASED = 'DECEASED', 'Deceased'
    SUSPENDED = 'SUSPENDED', 'Suspended'

def get_current_date():
    """Return current date (without time) for default values"""
    return timezone.now().date()

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email field must be set'))
        
        if password is None:
            raise ValidationError(_('A password must be provided'))
            
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_email_verified', False)
        extra_fields.setdefault('role', Role.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        if password is None:
            raise ValidationError(_('A password must be provided for superuser'))

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    # Basic Information
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    
    # Phone number with standardized regex
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    
    # Authentication Fields
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    mfa_enabled = models.BooleanField(default=False)
    
    # Role and Membership Information
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.MEMBER)
    member_id = models.CharField(max_length=20, unique=True, blank=True)
    primary_ministry = models.CharField(max_length=20, choices=Ministry.choices, blank=True, null=True)
    membership_start_date = models.DateField(default=get_current_date)
    baptized = models.BooleanField(default=False)
    
    # Basic Personal Information (detailed info moved to profile)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=Gender.choices, blank=True)
    
    # Tracking Information
    login_ip_address = models.GenericIPAddressField(null=True, blank=True)
    registration_ip_address = models.GenericIPAddressField(null=True, blank=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    def generate_member_id(self):
        """Generate member ID in the format GCAG-25-US-8X4D"""
        year_code = str(timezone.now().year)[-2:]
        ministry_code = self.primary_ministry if self.primary_ministry else 'GEN'
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return f"GCAG-{year_code}-{ministry_code}-{random_part}"

    def save(self, *args, **kwargs):
        if not self.member_id:
            self.member_id = self.generate_member_id()
        super().save(*args, **kwargs)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    @property
    def age(self):
        """Calculate age from date of birth"""
        if self.date_of_birth:
            from datetime import date
            today = date.today()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None