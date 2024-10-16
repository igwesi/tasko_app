from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
# Create your views here.


class api_view(APIView):
    def get(self, request):
        return Response({"message": "Tasko API!"})