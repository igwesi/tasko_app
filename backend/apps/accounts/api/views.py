from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.Profile.models import Profile
from apps.Profile.api.serializers import ProfileSerializer, SocialLinkSerializer, SkillSerializer

from .serializers import (
    # UserChangePasswordErrorSerializer,
    # UserChangePasswordSerializer,
    # UserCreateErrorSerializer,
    # UserCreateSerializer,
    # UserCurrentErrorSerializer,
    UserCurrentSerializer,
)

User = get_user_model()


class UserView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserCurrentSerializer

    def get(self, request):
        user    = UserCurrentSerializer(request.user).data
        profile = ProfileSerializer(Profile.objects.get(pk=request.user.profile.pk)).data
        skills  = SkillSerializer(request.user.profile.skills.all(), many=True).data
        social_links = SocialLinkSerializer(request.user.social_links.all(), many=True).data
        
        return Response({
            "user": user, 
            'profile':profile, 
            'skills': skills,
            'socials':social_links,
        }, status=status.HTTP_200_OK)