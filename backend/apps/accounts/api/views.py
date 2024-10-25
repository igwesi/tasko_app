from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import (
    action, 
    api_view, 
    renderer_classes,
    permission_classes, 
)

from django.contrib.auth import get_user_model
from apps.Profile.models import Profile
from .renderers import UserRenderer
from apps.Profile.api.serializers import ProfileSerializer, SocialLinkSerializer, SkillSerializer

from .serializers import (
    UserCurrentSerializer,
    UserCreateSerializer,
    LoginSerializer,
)

User = get_user_model()

def get_auth_tokens(user):
    refresh = RefreshToken.for_user(user)
    return{
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }

class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        refresh_token = request.data.get("refresh")
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                return Response({
                    "status":"success",
                    "access": str(token.access_token)
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    "status":"error",  
                    "msg": str(e)
                    }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "status":"error",
            "msg":"Refresh token not provided"
        }, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserCurrentSerializer

    def get(self, request):
        try:
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
        
        except Exception as e:
            return Response({
                "status":"error", 
                "msg": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    

class UserLogin(APIView):
    serializer_class = LoginSerializer()
    permission_classes = [AllowAny]
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user   = serializer.validated_data.get("user")
            message = serializer.validated_data.get("message")
            
            if user is not None:
                token = get_auth_tokens(user)
                
                return Response({
                    "status":"success", 
                    "token": token,
                    "message": "Logged in Successfully!"
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status":"error",
                    "message":message
                }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "status":"error", 
            "message":"Form submission invalid!",
        }, status=status.HTTP_400_BAD_REQUEST)


class UserRegister(APIView):
    permission_classes  = [AllowAny]
    serializer_class    = UserCreateSerializer
    renderer_classes    = [UserRenderer]

    def post(self, request, format=None):
        print(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        message = serializer.validated_data.get("message")

        if user is not None:
            token = get_auth_tokens(user)
            return Response({
                "status":"successful", 
                "token": token,
                "message": "Logged in Successfully!"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status":"error",
                "message":message
            }, status=status.HTTP_404_NOT_FOUND)