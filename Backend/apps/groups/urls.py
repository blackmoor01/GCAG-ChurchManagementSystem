from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.groups.views.groups import GroupViewSet, GroupMeetingViewSet

router = DefaultRouter()
router.register(r'', GroupViewSet, basename='group')
router.register(r'meetings', GroupMeetingViewSet, basename='group-meeting')

urlpatterns = [
    path('', include(router.urls)),
]