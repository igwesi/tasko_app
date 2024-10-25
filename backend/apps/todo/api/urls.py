from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.TodoList.as_view(), name="todos"),
    path('<int:pk>/', views.TodoDetail.as_view(), name="todos"),
    # path('todos/<int:pk>/', views.TodosDetail.as_view(), name="todo-detail"),
    # path("project/", views.ProjectView.as_view(), name="projects"),
]