from django.db import models
from django.core.validators import RegexValidator
from apps.users.models import User

class MemberProfile(models.Model):
    MARITAL_STATUS_CHOICES = [
        ('SINGLE', 'Single'),
        ('MARRIED', 'Married'), 
        ('DIVORCED', 'Divorced'),
        ('WIDOWED', 'Widowed'),
        ('SEPARATED', 'Separated'),
    ]
    
    MEMBERSHIP_STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('TRANSFERRED', 'Transferred'),
        ('DECEASED', 'Deceased'),
        ('SUSPENDED', 'Suspended'),
    ]
    
    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member_profile')
    
    # Personal Details
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, default='SINGLE')
    occupation = models.CharField(max_length=100, blank=True)
    employer = models.CharField(max_length=100, blank=True)
    education = models.CharField(max_length=100, blank=True)
    
    # Contact Information
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    alternative_phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=50, default='Ghana')
    
    # Spiritual Journey
    salvation_date = models.DateField(null=True, blank=True)
    baptism_date = models.DateField(null=True, blank=True)
    confirmation_date = models.DateField(null=True, blank=True)
    spiritual_gifts = models.JSONField(default=list)  # ['Teaching', 'Leadership', etc.]
    ministry_interests = models.JSONField(default=list)  # Areas of interest for ministry
    volunteer_skills = models.JSONField(default=list)  # Skills available for volunteering
    
    # Family Connections
    spouse = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='spouse_of')
    children = models.ManyToManyField(User, blank=True, related_name='parents')
    emergency_contact = models.JSONField(default=dict)  # {name, phone, relationship, address}
    
    # Membership Details
    membership_status = models.CharField(max_length=20, choices=MEMBERSHIP_STATUS_CHOICES, default='ACTIVE')
    membership_date = models.DateField(auto_now_add=True)
    transfer_date = models.DateField(null=True, blank=True)
    previous_church = models.CharField(max_length=200, blank=True)
    membership_notes = models.TextField(blank=True)
    
    # Preferences
    preferred_contact_method = models.CharField(max_length=20, choices=[
        ('EMAIL', 'Email'),
        ('PHONE', 'Phone'),
        ('SMS', 'SMS'),
        ('WHATSAPP', 'WhatsApp'),
    ], default='EMAIL')
    newsletter_subscription = models.BooleanField(default=True)
    event_notifications = models.BooleanField(default=True)
    
    # Additional Metadata
    profile_picture = models.URLField(blank=True)
    bio = models.TextField(blank=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_profiles')
    
    class Meta:
        ordering = ['user__first_name', 'user__last_name']
        indexes = [
            models.Index(fields=['membership_status']),
            models.Index(fields=['marital_status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.get_full_name()}'s Profile"
    
    @property
    def age(self):
        if self.date_of_birth:
            from datetime import date
            today = date.today()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None
    
    @property
    def full_address(self):
        address_parts = [self.address, self.city, self.state, self.postal_code, self.country]
        return ', '.join(filter(None, address_parts))

class MemberFamily(models.Model):
    """Model to handle family relationships more systematically"""
    head_of_family = models.ForeignKey(User, on_delete=models.CASCADE, related_name='family_head')
    family_name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, through='FamilyMembership', related_name='families')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Member Families"
    
    def __str__(self):
        return f"{self.family_name} Family"

class FamilyMembership(models.Model):
    """Through model for family relationships"""
    RELATIONSHIP_CHOICES = [
        ('HEAD', 'Head of Family'),
        ('SPOUSE', 'Spouse'),
        ('CHILD', 'Child'),
        ('PARENT', 'Parent'),
        ('SIBLING', 'Sibling'),
        ('RELATIVE', 'Other Relative'),
    ]
    
    family = models.ForeignKey(MemberFamily, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES)
    added_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['family', 'member']

class MemberNote(models.Model):
    """Model for pastoral notes and member interactions"""
    NOTE_TYPES = [
        ('GENERAL', 'General Note'),
        ('PASTORAL', 'Pastoral Care'),
        ('COUNSELING', 'Counseling Session'),
        ('PRAYER', 'Prayer Request'),
        ('VISIT', 'Home Visit'),
        ('PHONE', 'Phone Call'),
        ('MEETING', 'Meeting'),
    ]
    
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='member_notes')
    note_type = models.CharField(max_length=20, choices=NOTE_TYPES, default='GENERAL')
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_confidential = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_notes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.member.get_full_name()}"

class MemberSkill(models.Model):
    """Model to track member skills and talents"""
    SKILL_CATEGORIES = [
        ('MINISTRY', 'Ministry'),
        ('TECHNICAL', 'Technical'),
        ('CREATIVE', 'Creative'),
        ('ADMINISTRATIVE', 'Administrative'),
        ('PROFESSIONAL', 'Professional'),
        ('PRACTICAL', 'Practical'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=SKILL_CATEGORIES)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class MemberSkillAssignment(models.Model):
    """Through model for member skills"""
    PROFICIENCY_LEVELS = [
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced'),
        ('EXPERT', 'Expert'),
    ]
    
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skill_assignments')
    skill = models.ForeignKey(MemberSkill, on_delete=models.CASCADE)
    proficiency_level = models.CharField(max_length=20, choices=PROFICIENCY_LEVELS, default='BEGINNER')
    years_of_experience = models.PositiveIntegerField(default=0)
    is_willing_to_serve = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    assigned_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['member', 'skill']