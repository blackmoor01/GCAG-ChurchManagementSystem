from django.contrib import admin
from .models import Group, GroupMembership, GroupMeeting, GroupAttendance

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'ministry_type', 'group_type', 'member_count', 'is_active']
    list_filter = ['ministry_type', 'group_type', 'is_active', 'is_open_to_new_members']
    search_fields = ['name', 'description']
    filter_horizontal = ['leaders']

@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ['member', 'group', 'role', 'status', 'date_joined']
    list_filter = ['role', 'status', 'date_joined']
    search_fields = ['member__first_name', 'member__last_name', 'group__name']

@admin.register(GroupMeeting)
class GroupMeetingAdmin(admin.ModelAdmin):
    list_display = ['title', 'group', 'date', 'is_cancelled']
    list_filter = ['group', 'date', 'is_cancelled']
    search_fields = ['title', 'group__name']

@admin.register(GroupAttendance)
class GroupAttendanceAdmin(admin.ModelAdmin):
    list_display = ['member', 'meeting', 'present', 'recorded_at']
    list_filter = ['present', 'meeting__date']
    search_fields = ['member__first_name', 'member__last_name', 'meeting__title']