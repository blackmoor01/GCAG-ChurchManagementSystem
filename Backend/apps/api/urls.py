from django.urls import path, include

urlpatterns = [
    # Users API endpoints
    path('users/', include('apps.users.urls')),

    # Members API endpoints
    path('members/', include('apps.members.urls')),

    # Groups API endpoints
    path('groups/', include('apps.groups.urls')),
    
]