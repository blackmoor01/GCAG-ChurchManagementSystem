from django.contrib import admin
from .models import (
    MemberProfile, MemberFamily, FamilyMembership,
    MemberNote, MemberSkill, MemberSkillAssignment
)

@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'membership_status', 'marital_status', 'get_gender', 'city', 'created_at']
    list_filter = ['membership_status', 'marital_status', 'user__gender', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'phone_number']
    readonly_fields = ['created_at', 'updated_at']


    def get_gender(self, obj):
        return obj.user.get_gender_display()
    get_gender.short_description = 'Gender'
    get_gender.admin_order_field = 'user__gender'
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Personal Details', {
            'fields': ('get_gender', 'date_of_birth', 'marital_status', 'occupation', 'employer', 'education')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'alternative_phone', 'address', 'city', 'state', 'postal_code', 'country')
        }),
        ('Spiritual Journey', {
            'fields': ('salvation_date', 'baptism_date', 'confirmation_date', 'spiritual_gifts', 'ministry_interests', 'volunteer_skills')
        }),
        ('Family Connections', {
            'fields': ('spouse', 'children', 'emergency_contact')
        }),
        ('Membership', {
            'fields': ('membership_status', 'membership_date', 'transfer_date', 'previous_church', 'membership_notes')
        }),
        ('Preferences', {
            'fields': ('preferred_contact_method', 'newsletter_subscription', 'event_notifications')
        }),
        ('Additional Info', {
            'fields': ('profile_picture', 'bio', 'created_by', 'created_at', 'updated_at')
        }),
    )

@admin.register(MemberFamily)
class MemberFamilyAdmin(admin.ModelAdmin):
    list_display = ['family_name', 'head_of_family', 'member_count', 'created_at']
    search_fields = ['family_name', 'head_of_family__first_name', 'head_of_family__last_name']
    
    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Members'

@admin.register(MemberNote)
class MemberNoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'member', 'note_type', 'is_confidential', 'created_by', 'created_at']
    list_filter = ['note_type', 'is_confidential', 'created_at']
    search_fields = ['title', 'member__first_name', 'member__last_name', 'content']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(MemberSkill)
class MemberSkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'description']

@admin.register(MemberSkillAssignment)
class MemberSkillAssignmentAdmin(admin.ModelAdmin):
    list_display = ['member', 'skill', 'proficiency_level', 'is_willing_to_serve', 'assigned_date']
    list_filter = ['proficiency_level', 'is_willing_to_serve', 'skill__category']
    search_fields = ['member__first_name', 'member__last_name', 'skill__name']