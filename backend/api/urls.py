from django.urls import path, include
from .views import API

urlpatterns = [
    path('', API.as_view(), name="api"),
]