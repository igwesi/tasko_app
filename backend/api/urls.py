from django.urls import path, include
from .views import *

urlpatterns = [
    path('', api_view.as_view()),
]