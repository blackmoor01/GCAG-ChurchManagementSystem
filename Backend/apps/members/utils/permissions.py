from rest_framework.permissions import BasePermission

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
            hasattr(request.user, 'profile') and 
            request.user.profile.get('is_pastoral_staff', False)
        )
