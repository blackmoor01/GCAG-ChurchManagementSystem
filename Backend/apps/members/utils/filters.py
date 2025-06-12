import django_filters
from django.contrib.auth import get_user_model
from apps.members.models import MemberProfile
from apps.users.models import Gender, MaritalStatus, MembershipStatus

User = get_user_model()

class MemberProfileFilter(django_filters.FilterSet):
    
    membership_status = django_filters.ChoiceFilter(choices=MembershipStatus.choices)
    marital_status = django_filters.ChoiceFilter(choices=MaritalStatus.choices)
    
    # Gender filter now references the User model
    gender = django_filters.ChoiceFilter(
        field_name='user__gender', 
        choices=Gender.choices
    )
    
    city = django_filters.CharFilter(lookup_expr='icontains')
    
    
    age_min = django_filters.NumberFilter(
        field_name='user__date_of_birth', 
        lookup_expr='lte',
        method='filter_age_min'
    )
    age_max = django_filters.NumberFilter(
        field_name='user__date_of_birth', 
        lookup_expr='gte',
        method='filter_age_max'
    )
    
    has_spouse = django_filters.BooleanFilter(
        field_name='spouse', 
        lookup_expr='isnull', 
        exclude=True
    )
    
    # Additional useful filters
    primary_ministry = django_filters.ChoiceFilter(
        field_name='user__primary_ministry',
        choices=User._meta.get_field('primary_ministry').choices
    )
    
    baptized = django_filters.BooleanFilter(field_name='user__baptized')
    
    # Search filters
    name_search = django_filters.CharFilter(method='filter_name_search')
    email_search = django_filters.CharFilter(
        field_name='user__email', 
        lookup_expr='icontains'
    )
    phone_search = django_filters.CharFilter(
        field_name='user__phone_number', 
        lookup_expr='icontains'
    )
    
    class Meta:
        model = MemberProfile
        fields = [
            'membership_status', 
            'marital_status', 
            'city', 
            'baptized',
            'primary_ministry'
        ]
    
    def filter_age_min(self, queryset, name, value):
        """Filter for minimum age"""
        if value:
            from datetime import date, timedelta
            max_birth_date = date.today() - timedelta(days=value * 365.25)
            return queryset.filter(user__date_of_birth__lte=max_birth_date)
        return queryset
    
    def filter_age_max(self, queryset, name, value):
        """Filter for maximum age"""
        if value:
            from datetime import date, timedelta
            min_birth_date = date.today() - timedelta(days=value * 365.25)
            return queryset.filter(user__date_of_birth__gte=min_birth_date)
        return queryset
    
    def filter_name_search(self, queryset, name, value):
        """Search across first name and last name"""
        if value:
            from django.db.models import Q
            return queryset.filter(
                Q(user__first_name__icontains=value) |
                Q(user__last_name__icontains=value)
            )
        return queryset