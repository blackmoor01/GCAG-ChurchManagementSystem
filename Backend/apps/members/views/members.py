from rest_framework import status, generics, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model

from apps.members.models import (
    MemberProfile, MemberFamily, FamilyMembership,
    MemberNote, MemberSkill, MemberSkillAssignment
)
from apps.members.serializers.members import (
    MemberProfileSerializer, MemberProfileListSerializer,
    MemberFamilySerializer, MemberNoteSerializer,
    MemberSkillSerializer, MemberSkillAssignmentSerializer
)
from apps.members.utils.filters import MemberProfileFilter
from apps.members.utils.permissions import IsPastoralStaffOrReadOnly

User = get_user_model()

class MemberProfileListCreateView(generics.ListCreateAPIView):
    """
    GET: List all member profiles with filtering and search
    POST: Create new member profile
    """
    queryset = MemberProfile.objects.select_related('user', 'spouse').prefetch_related('children')
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MemberProfileFilter
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'occupation', 'city']
    ordering_fields = ['created_at', 'user__first_name', 'membership_date']
    ordering = ['user__first_name']
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MemberProfileListSerializer
        return MemberProfileSerializer
    
    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            created_by=self.request.user
        )

class MemberProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve specific member profile
    PUT: Update entire member profile
    PATCH: Partially update member profile
    DELETE: Soft delete member profile (set inactive)
    """
    queryset = MemberProfile.objects.select_related('user', 'spouse').prefetch_related('children')
    serializer_class = MemberProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    
    def perform_destroy(self, instance):
        # Soft delete - set membership status to inactive
        instance.membership_status = 'INACTIVE'
        instance.save()

class MemberSearchView(APIView):
    """
    GET: Advanced search for members
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        query = request.GET.get('q', '')
        filters = {}
        
        # Build dynamic filters from query parameters
        if request.GET.get('membership_status'):
            filters['membership_status'] = request.GET.get('membership_status')
        if request.GET.get('marital_status'):
            filters['marital_status'] = request.GET.get('marital_status')
        if request.GET.get('gender'):
            filters['gender'] = request.GET.get('gender')
        if request.GET.get('city'):
            filters['city__icontains'] = request.GET.get('city')
        
        # Text search across multiple fields
        profiles = MemberProfile.objects.filter(**filters)
        if query:
            profiles = profiles.filter(
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(user__email__icontains=query) |
                Q(occupation__icontains=query) |
                Q(phone_number__icontains=query)
            )
        
        profiles = profiles.select_related('user').order_by('user__first_name')[:50]
        serializer = MemberProfileListSerializer(profiles, many=True)
        
        return Response({
            'count': profiles.count(),
            'results': serializer.data
        })

class MemberStatsView(APIView):
    """
    GET: Get membership statistics
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        total_members = MemberProfile.objects.count()
        active_members = MemberProfile.objects.filter(membership_status='ACTIVE').count()
        
        # Demographics
        gender_stats = MemberProfile.objects.values('gender').annotate(count=Count('id'))
        marital_stats = MemberProfile.objects.values('marital_status').annotate(count=Count('id'))
        membership_stats = MemberProfile.objects.values('membership_status').annotate(count=Count('id'))
        
        # Age groups (simplified)
        from datetime import date, timedelta
        today = date.today()
        children = MemberProfile.objects.filter(
            date_of_birth__gte=today - timedelta(days=18*365)
        ).count()
        youth = MemberProfile.objects.filter(
            date_of_birth__gte=today - timedelta(days=35*365),
            date_of_birth__lt=today - timedelta(days=18*365)
        ).count()
        adults = MemberProfile.objects.filter(
            date_of_birth__lt=today - timedelta(days=35*365)
        ).count()
        
        return Response({
            'total_members': total_members,
            'active_members': active_members,
            'inactive_members': total_members - active_members,
            'demographics': {
                'gender': list(gender_stats),
                'marital_status': list(marital_stats),
                'membership_status': list(membership_stats),
                'age_groups': {
                    'children': children,
                    'youth': youth,
                    'adults': adults
                }
            }
        })

class MemberFamilyViewSet(APIView):
    """
    Handle family management operations
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, family_id=None):
        if family_id:
            family = get_object_or_404(MemberFamily, id=family_id)
            serializer = MemberFamilySerializer(family)
            return Response(serializer.data)
        
        families = MemberFamily.objects.prefetch_related('members').order_by('family_name')
        serializer = MemberFamilySerializer(families, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """Create new family"""
        data = request.data.copy()
        family = MemberFamily.objects.create(
            head_of_family_id=data['head_of_family_id'],
            family_name=data['family_name']
        )
        
        # Add family members
        if 'members' in data:
            for member_data in data['members']:
                FamilyMembership.objects.create(
                    family=family,
                    member_id=member_data['member_id'],
                    relationship=member_data['relationship']
                )
        
        serializer = MemberFamilySerializer(family)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MemberNoteViewSet(APIView):
    """
    Handle member notes operations
    """
    permission_classes = [IsAuthenticated, IsPastoralStaffOrReadOnly]
    
    def get(self, request, member_id):
        notes = MemberNote.objects.filter(member_id=member_id).order_by('-created_at')
        
        # Filter confidential notes for non-pastoral staff
        if not request.user.is_staff:
            notes = notes.filter(is_confidential=False)
        
        serializer = MemberNoteSerializer(notes, many=True)
        return Response(serializer.data)
    
    def post(self, request, member_id):
        """Add note to member"""
        data = request.data.copy()
        data['member'] = member_id
        
        note = MemberNote.objects.create(
            member_id=member_id,
            note_type=data.get('note_type', 'GENERAL'),
            title=data['title'],
            content=data['content'],
            is_confidential=data.get('is_confidential', False),
            created_by=request.user
        )
        
        serializer = MemberNoteSerializer(note)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MemberSkillManagementView(APIView):
    """
    Handle member skills management
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, member_id=None):
        if member_id:
            # Get skills for specific member
            assignments = MemberSkillAssignment.objects.filter(
                member_id=member_id
            ).select_related('skill')
            serializer = MemberSkillAssignmentSerializer(assignments, many=True)
            return Response(serializer.data)
        
        # Get all available skills
        skills = MemberSkill.objects.filter(is_active=True).order_by('category', 'name')
        serializer = MemberSkillSerializer(skills, many=True)
        return Response(serializer.data)
    
    def post(self, request, member_id):
        """Assign skill to member"""
        data = request.data
        assignment, created = MemberSkillAssignment.objects.get_or_create(
            member_id=member_id,
            skill_id=data['skill_id'],
            defaults={
                'proficiency_level': data.get('proficiency_level', 'BEGINNER'),
                'years_of_experience': data.get('years_of_experience', 0),
                'is_willing_to_serve': data.get('is_willing_to_serve', True),
                'notes': data.get('notes', '')
            }
        )
        
        if not created:
            # Update existing assignment
            for field in ['proficiency_level', 'years_of_experience', 'is_willing_to_serve', 'notes']:
                if field in data:
                    setattr(assignment, field, data[field])
            assignment.save()
        
        serializer = MemberSkillAssignmentSerializer(assignment)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)