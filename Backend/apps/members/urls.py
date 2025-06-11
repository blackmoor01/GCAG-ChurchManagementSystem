from django.urls import path
from apps.members.views.members import (
    MemberProfileListCreateView,
    MemberProfileDetailView,
    MemberSearchView,
    MemberStatsView,
    MemberFamilyViewSet,
    MemberNoteViewSet,
    MemberSkillManagementView, 
)


urlpatterns = [
    # Member Profiles
    path('profiles/', MemberProfileListCreateView.as_view(), name='member-profile-list-create'),
    path('profiles/<int:id>/', MemberProfileDetailView.as_view(), name='member-profile-detail'),
    
    # Member Search & Stats
    path('profiles/search/', MemberSearchView.as_view(), name='member-profile-search'),
    path('profiles/stats/', MemberStatsView.as_view(), name='member-profile-stats'),

    # Member Families
    path('families/', MemberFamilyViewSet.as_view(), name='member-family-list-create'),
    path('families/<int:family_id>/', MemberFamilyViewSet.as_view(), name='member-family-detail'),

    # Member Notes
    path('profiles/<int:member_id>/notes/', MemberNoteViewSet.as_view(), name='member-notes'),

    # Member Skills
    path('profiles/<int:member_id>/skills/', MemberSkillManagementView.as_view(), name='member-skills'),
    path('skills/', MemberSkillManagementView.as_view(), name='all-member-skills'),
]