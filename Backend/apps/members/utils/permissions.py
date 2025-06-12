from rest_framework.permissions import BasePermission
from apps.users.models import Role

class IsPastoralStaffOrReadOnly(BasePermission):
    """
    Custom permission to only allow pastoral staff to edit certain sensitive information
    """
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return request.user.is_authenticated
        
        # For write operations, check if user is pastoral staff
        return request.user.is_authenticated and (
            request.user.is_staff or 
            request.user.role in [Role.ADMIN, Role.HEAD_PASTOR]
        )

class IsMemberOwnerOrPastoralStaff(BasePermission):
    """
    Custom permission to allow members to view/edit their own profile 
    or pastoral staff to view/edit any profile
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Members can access their own profile
        if hasattr(obj, 'user') and obj.user == request.user:
            return True
        
        # If the object is a User instance
        if obj == request.user:
            return True
            
        # Pastoral staff can access any profile
        if (request.user.is_staff or 
            request.user.role in [Role.ADMIN, Role.HEAD_PASTOR]):
            return True
            
        return False

class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admins to make changes
    """
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return request.user.is_authenticated
        
        return (request.user.is_authenticated and 
                request.user.role == Role.ADMIN)

class IsMinistryLeaderOrAdmin(BasePermission):
    """
    Permission for ministry-specific operations
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        # Admins have full access
        if request.user.role == Role.ADMIN:
            return True
            
        # Check if user is a ministry leader
        # This could check if the user leads any groups in their ministry
        return hasattr(request.user, 'led_groups') and request.user.led_groups.exists()

class CanViewMemberNotes(BasePermission):
    """
    Permission for viewing member notes (pastoral care)
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff or
            request.user.role in [Role.ADMIN, Role.HEAD_PASTOR]
        )
    
    def has_object_permission(self, request, view, obj):
        # Only allow viewing if user has pastoral permissions
        # and if the note is not confidential or user is admin/head pastor
        if not (request.user.is_staff or 
                request.user.role in [Role.ADMIN, Role.HEAD_PASTOR]):
            return False
            
        # Confidential notes only for admin and head pastor
        if obj.is_confidential and request.user.role not in [Role.ADMIN, Role.HEAD_PASTOR]:
            return False
            
        return True