from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

# Create your views here.

class API(APIView):
    permission_classes = [AllowAny]
    @extend_schema(responses={200: OpenApiTypes.STR})

    def get(self, request):
        """Return a simple message indicating that the API is live."""
        return Response({"message": "Tasko API is Live!"})
