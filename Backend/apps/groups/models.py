# apps/groups/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

User = get_user_model()

class GroupMinistry(models.TextChoices):
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

class GroupType(models.TextChoices):
    SMALL_GROUP = 'SMALL_GROUP', 'Small Group'
    MINISTRY_TEAM = 'MINISTRY_TEAM', 'Ministry Team'
    BIBLE_STUDY = 'BIBLE_STUDY', 'Bible Study'
    PRAYER_GROUP = 'PRAYER_GROUP', 'Prayer Group'
    SERVICE_TEAM = 'SERVICE_TEAM', 'Service Team'
    CHOIR = 'CHOIR', 'Choir'
    COMMITTEE = 'COMMITTEE', 'Committee'

class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    ministry_type = models.CharField(max_length=20, choices=GroupMinistry.choices)
    group_type = models.CharField(max_length=20, choices=GroupType.choices, default=GroupType.SMALL_GROUP)
    
    # Leadership
    leaders = models.ManyToManyField(User, related_name='led_groups', blank=True)
    members = models.ManyToManyField(
        User, 
        related_name='member_groups', 
        through='GroupMembership',
        through_fields=('group', 'member')
    )
    
    # Meeting Information
    meeting_schedule = models.JSONField(default=dict)  # {day: "Tuesday", time: "19:00", frequency: "weekly"}
    meeting_location = models.CharField(max_length=200, blank=True)
    max_capacity = models.PositiveIntegerField(null=True, blank=True)
    
    # Group Settings
    is_active = models.BooleanField(default=True)
    is_open_to_new_members = models.BooleanField(default=True)
    requires_approval = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_groups')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def member_count(self):
        return self.groupmembership_set.filter(status='ACTIVE').count()

    @property
    def is_at_capacity(self):
        if self.max_capacity:
            return self.member_count >= self.max_capacity
        return False

    def can_user_join(self, user):
        """Check if user can join this group"""
        if not self.is_active or not self.is_open_to_new_members:
            return False
        if self.is_at_capacity:
            return False
        if self.groupmembership_set.filter(member=user, status='ACTIVE').exists():
            return False
        return True

class GroupMembership(models.Model):
    ROLE_CHOICES = [
        ('MEMBER', 'Member'),
        ('LEADER', 'Leader'),
        ('CO_LEADER', 'Co-Leader'),
        ('ASSISTANT', 'Assistant Leader'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('PENDING', 'Pending Approval'),
        ('REMOVED', 'Removed'),
    ]

    member = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField(auto_now_add=True)
    date_left = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='MEMBER')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    
    # Additional fields
    notes = models.TextField(blank=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='added_memberships')

    class Meta:
        unique_together = ('member', 'group')
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.member.get_full_name()} - {self.group.name} ({self.role})"

class GroupMeeting(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='meetings')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True)
    duration_minutes = models.PositiveIntegerField(default=60)
    
    # Meeting status
    is_cancelled = models.BooleanField(default=False)
    cancellation_reason = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.group.name} - {self.title} ({self.date.strftime('%Y-%m-%d')})"

class GroupAttendance(models.Model):
    meeting = models.ForeignKey(GroupMeeting, on_delete=models.CASCADE, related_name='attendance_records')
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    present = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='recorded_attendance')

    class Meta:
        unique_together = ('meeting', 'member')

    def __str__(self):
        status = "Present" if self.present else "Absent"
        return f"{self.member.get_full_name()} - {self.meeting.title} ({status})"