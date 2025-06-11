from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.members.models import (
    MemberProfile, MemberFamily, FamilyMembership, 
    MemberNote, MemberSkill, MemberSkillAssignment
)

User = get_user_model()

class UserBasicSerializer(serializers.ModelSerializer):
    """Basic user info for related fields"""
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name']

class MemberProfileSerializer(serializers.ModelSerializer):
    user = UserBasicSerializer(read_only=True)
    spouse = UserBasicSerializer(read_only=True)
    children = UserBasicSerializer(many=True, read_only=True)
    age = serializers.ReadOnlyField()
    full_address = serializers.ReadOnlyField()
    
    # Write-only fields for relationships
    spouse_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    children_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = MemberProfile
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by', 'membership_date']
    
    def create(self, validated_data):
        spouse_id = validated_data.pop('spouse_id', None)
        children_ids = validated_data.pop('children_ids', [])
        
        profile = MemberProfile.objects.create(**validated_data)
        
        if spouse_id:
            try:
                spouse = User.objects.get(id=spouse_id)
                profile.spouse = spouse
                profile.save()
            except User.DoesNotExist:
                pass
        
        if children_ids:
            children = User.objects.filter(id__in=children_ids)
            profile.children.set(children)
        
        return profile
    
    def update(self, instance, validated_data):
        spouse_id = validated_data.pop('spouse_id', None)
        children_ids = validated_data.pop('children_ids', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if spouse_id is not None:
            if spouse_id:
                try:
                    spouse = User.objects.get(id=spouse_id)
                    instance.spouse = spouse
                except User.DoesNotExist:
                    instance.spouse = None
            else:
                instance.spouse = None
            instance.save()
        
        if children_ids is not None:
            children = User.objects.filter(id__in=children_ids)
            instance.children.set(children)
        
        return instance

class MemberProfileListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""
    user = UserBasicSerializer(read_only=True)
    age = serializers.ReadOnlyField()
    
    class Meta:
        model = MemberProfile
        fields = [
            'id', 'user', 'gender', 'age', 'marital_status', 
            'occupation', 'membership_status', 'phone_number', 'city'
        ]

class FamilyMembershipSerializer(serializers.ModelSerializer):
    member = UserBasicSerializer(read_only=True)
    
    class Meta:
        model = FamilyMembership
        fields = ['id', 'member', 'relationship', 'added_date']

class MemberFamilySerializer(serializers.ModelSerializer):
    head_of_family = UserBasicSerializer(read_only=True)
    family_members = FamilyMembershipSerializer(source='familymembership_set', many=True, read_only=True)
    member_count = serializers.SerializerMethodField()
    
    class Meta:
        model = MemberFamily
        fields = '__all__'
    
    def get_member_count(self, obj):
        return obj.members.count()

class MemberNoteSerializer(serializers.ModelSerializer):
    member = UserBasicSerializer(read_only=True)
    created_by = UserBasicSerializer(read_only=True)
    
    class Meta:
        model = MemberNote
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by']

class MemberSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberSkill
        fields = '__all__'

class MemberSkillAssignmentSerializer(serializers.ModelSerializer):
    member = UserBasicSerializer(read_only=True)
    skill = MemberSkillSerializer(read_only=True)
    
    class Meta:
        model = MemberSkillAssignment
        fields = '__all__'
        read_only_fields = ['assigned_date']
