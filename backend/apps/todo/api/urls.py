from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.TodosList.as_view()),
    path('todos/<int:pk>/', views.TodosDetail.as_view()),
    path("projects/", views.ProjectsList.as_view()),
]