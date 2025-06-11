import django_filters
from apps.members.models import MemberProfile

class MemberProfileFilter(django_filters.FilterSet):
    membership_status = django_filters.ChoiceFilter(choices=MemberProfile.MEMBERSHIP_STATUS_CHOICES)
    marital_status = django_filters.ChoiceFilter(choices=MemberProfile.MARITAL_STATUS_CHOICES)
    gender = django_filters.ChoiceFilter(choices=MemberProfile.GENDER_CHOICES)
    city = django_filters.CharFilter(lookup_expr='icontains')
    age_min = django_filters.NumberFilter(field_name='date_of_birth', lookup_expr='lte')
    age_max = django_filters.NumberFilter(field_name='date_of_birth', lookup_expr='gte')
    has_spouse = django_filters.BooleanFilter(field_name='spouse', lookup_expr='isnull', exclude=True)
    
    class Meta:
        model = MemberProfile
        fields = ['membership_status', 'marital_status', 'gender', 'city']