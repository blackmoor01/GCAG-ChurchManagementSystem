from rest_framework import serializers
from apps.groups.models import Group, GroupMembership, GroupMeeting, GroupAttendance

class GroupMembershipSerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source='member.get_full_name', read_only=True)
    member_email = serializers.CharField(source='member.email', read_only=True)

    class Meta:
        model = GroupMembership
        fields = ['id', 'member', 'member_name', 'member_email', 'date_joined', 
                 'role', 'status', 'notes']

class GroupSerializer(serializers.ModelSerializer):
    member_count = serializers.ReadOnlyField()
    is_at_capacity = serializers.ReadOnlyField()
    leaders_details = serializers.SerializerMethodField()
    
    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'ministry_type', 'group_type',
                 'meeting_schedule', 'meeting_location', 'max_capacity',
                 'is_active', 'is_open_to_new_members', 'requires_approval',
                 'member_count', 'is_at_capacity', 'leaders_details',
                 'created_at', 'updated_at']

    def get_leaders_details(self, obj):
        return [{'id': leader.id, 'name': leader.get_full_name(), 'email': leader.email} 
                for leader in obj.leaders.all()]

class GroupDetailSerializer(GroupSerializer):
    memberships = GroupMembershipSerializer(source='groupmembership_set', many=True, read_only=True)
    
    class Meta(GroupSerializer.Meta):
        fields = GroupSerializer.Meta.fields + ['memberships']

class GroupMeetingSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.name', read_only=True)
    attendance_count = serializers.SerializerMethodField()

    class Meta:
        model = GroupMeeting
        fields = ['id', 'group', 'group_name', 'title', 'description', 'date',
                 'location', 'duration_minutes', 'is_cancelled', 
                 'cancellation_reason', 'attendance_count', 'created_at']

    def get_attendance_count(self, obj):
        return obj.attendance_records.filter(present=True).count()

class GroupAttendanceSerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source='member.get_full_name', read_only=True)

    class Meta:
        model = GroupAttendance
        fields = ['id', 'meeting', 'member', 'member_name', 'present', 'notes']