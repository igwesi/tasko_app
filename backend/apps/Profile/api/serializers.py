from rest_framework import exceptions, serializers
from django.contrib.auth import get_user_model
from ..models import (
    Profile,
    Skill,
    SocialLink,
)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('bio', 'avatar')

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['name']

class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ['facebook', 'github', 'instagram', 'linkedin', 'reddit', 'telegram', 'twitch', 'tiktok', 'twitter']