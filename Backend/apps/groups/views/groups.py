from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count
from django.utils import timezone
from apps.groups.models import Group, GroupMembership, GroupMeeting, GroupAttendance
from apps.groups.serializers.groups import (GroupSerializer, GroupDetailSerializer, 
                         GroupMembershipSerializer, GroupMeetingSerializer,
                         GroupAttendanceSerializer)

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return GroupDetailSerializer
        return GroupSerializer

    def get_queryset(self):
        queryset = Group.objects.all()
        
        # Filter parameters
        ministry_type = self.request.query_params.get('ministry_type')
        group_type = self.request.query_params.get('group_type')
        is_active = self.request.query_params.get('is_active')
        search = self.request.query_params.get('search')

        if ministry_type:
            queryset = queryset.filter(ministry_type=ministry_type)
        if group_type:
            queryset = queryset.filter(group_type=group_type)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )

        return queryset

    @action(detail=True, methods=['post'])
    def join_group(self, request, pk=None):
        """Allow a user to join a group"""
        group = self.get_object()
        user = request.user

        if not group.can_user_join(user):
            return Response(
                {'error': 'Cannot join this group'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        membership_status = 'PENDING' if group.requires_approval else 'ACTIVE'
        
        membership, created = GroupMembership.objects.get_or_create(
            member=user,
            group=group,
            defaults={
                'status': membership_status,
                'added_by': user
            }
        )

        if not created:
            return Response(
                {'error': 'Already a member of this group'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({'message': 'Successfully joined group'})

    @action(detail=True, methods=['post'])
    def leave_group(self, request, pk=None):
        """Allow a user to leave a group"""
        group = self.get_object()
        user = request.user

        try:
            membership = GroupMembership.objects.get(member=user, group=group, status='ACTIVE')
            membership.status = 'INACTIVE'
            membership.date_left = timezone.now().date()
            membership.save()
            return Response({'message': 'Successfully left group'})
        except GroupMembership.DoesNotExist:
            return Response(
                {'error': 'Not a member of this group'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def approve_member(self, request, pk=None):
        """Approve a pending member (leaders only)"""
        group = self.get_object()
        member_id = request.data.get('member_id')

        # Check if user is a leader
        if not group.leaders.filter(id=request.user.id).exists():
            return Response(
                {'error': 'Only group leaders can approve members'}, 
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            membership = GroupMembership.objects.get(
                group=group, member_id=member_id, status='PENDING'
            )
            membership.status = 'ACTIVE'
            membership.save()
            return Response({'message': 'Member approved successfully'})
        except GroupMembership.DoesNotExist:
            return Response(
                {'error': 'Pending membership not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Get all members of a group"""
        group = self.get_object()
        memberships = group.groupmembership_set.filter(status='ACTIVE')
        serializer = GroupMembershipSerializer(memberships, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get group statistics"""
        group = self.get_object()
        
        stats = {
            'total_members': group.member_count,
            'leaders_count': group.leaders.count(),
            'recent_meetings': group.meetings.filter(
                date__gte=timezone.now() - timezone.timedelta(days=30)
            ).count(),
            'average_attendance': self._calculate_average_attendance(group)
        }
        
        return Response(stats)

    def _calculate_average_attendance(self, group):
        """Calculate average attendance for recent meetings"""
        recent_meetings = group.meetings.filter(
            date__gte=timezone.now() - timezone.timedelta(days=90)
        )
        
        if not recent_meetings.exists():
            return 0
        
        total_attendance = 0
        meeting_count = 0
        
        for meeting in recent_meetings:
            attendance_count = meeting.attendance_records.filter(present=True).count()
            total_attendance += attendance_count
            meeting_count += 1
        
        return round(total_attendance / meeting_count, 2) if meeting_count > 0 else 0

class GroupMeetingViewSet(viewsets.ModelViewSet):
    queryset = GroupMeeting.objects.all()
    serializer_class = GroupMeetingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = GroupMeeting.objects.all()
        group_id = self.request.query_params.get('group')
        
        if group_id:
            queryset = queryset.filter(group_id=group_id)
        
        return queryset

    @action(detail=True, methods=['post'])
    def record_attendance(self, request, pk=None):
        """Record attendance for a meeting"""
        meeting = self.get_object()
        attendance_data = request.data.get('attendance', [])
        
        # Check if user can record attendance (group leader or admin)
        if not meeting.group.leaders.filter(id=request.user.id).exists():
            if not request.user.is_staff:
                return Response(
                    {'error': 'Only group leaders can record attendance'}, 
                    status=status.HTTP_403_FORBIDDEN
                )

        recorded_count = 0
        for record in attendance_data:
            attendance, created = GroupAttendance.objects.update_or_create(
                meeting=meeting,
                member_id=record['member_id'],
                defaults={
                    'present': record['present'],
                    'notes': record.get('notes', ''),
                    'recorded_by': request.user
                }
            )
            recorded_count += 1

        return Response({
            'message': f'Attendance recorded for {recorded_count} members'
        })

    @action(detail=True, methods=['get'])
    def attendance(self, request, pk=None):
        """Get attendance records for a meeting"""
        meeting = self.get_object()
        attendance_records = meeting.attendance_records.all()
        serializer = GroupAttendanceSerializer(attendance_records, many=True)
        return Response(serializer.data)