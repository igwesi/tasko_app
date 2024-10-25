from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    TodoSerializer, 
    ProjectSerializer,
    UpdateTodoSerializer,
)
from ..models import Todo, Project
from django.db.models import Q


from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes



class TodoList(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = TodoSerializer

    @extend_schema(
        request=TodoSerializer,
        responses = TodoSerializer,
    )
        
    def get(self, request, pk=None):
        """
        Retrieve all todo items for the current user.

        Queries the Todo model for items where the owner is the current user,
        serializes the queryset, and returns the serialized data.

        Args:
            request: The HTTP request object containing user details.

        Returns:
            Response: A Response object containing the serialized todo data
                      and a status code of 200.
        """
        if pk:
            todo = self.get_object(pk)
            serialized = TodoSerializer(todo)
            return Response(serialized.data, status=status.HTTP_200_OK)
        else:
            user_todo_list = Todo.objects.filter(owner=request.user)
            serialized = TodoSerializer(user_todo_list, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """
        Create a new todo item for the current user.
        Args:
            request: The HTTP request object containing user details and todo data.
        Returns:
            Response: A Response object containing the serialized todo data
            and a status code of 201.
        """
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

class TodoDetail(APIView):
    """
        Retrieve, update or delete a todo item for the current user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class   = UpdateTodoSerializer

    @extend_schema(
        request=TodoSerializer,
        responses = TodoSerializer,
    )
    def get_object(self, pk):
        return Todo.objects.get(pk=pk)

    def get(self, request, pk, format=None):
        """
        Retrieve a todo item for the current user by its primary key.
        Args:
            request: The HTTP request object containing user details.
            pk: The primary key of the todo item to retrieve.
        Returns:
            Response: A Response object containing the serialized todo data
            and a status code of 200.
        """
        todo = self.get_object(pk)
        serialized = TodoSerializer(todo)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        """
        Update a todo item for the current user.
        Args:
            request: The HTTP request object containing user details and todo data.
            pk: The primary key of the todo item to update.
            format: The format of the request (optional).

        Returns:
            Response: A Response object containing the serialized todo data
                    if the update is successful, or the validation errors
                    and a status code of 400 if the update fails.
        """
        todo = self.get_object(pk)
        serializer = UpdateTodoSerializer(todo, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        todo = self.get_object(pk)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = ProjectSerializer

    def get(self, request, pk=None):
        """
        Retrieves all projects associated with the current user either as an owner or as a member.
        This method filters projects based on the current user's involvement, either as the owner or as a user in the project.
        
        It serializes the resulting project queryset and returns a response containing the serialized data and a message.
        
        Args:
            request: The HTTP request object containing the user details.
        Returns:
            Response: A Response object containing the serialized project data and a status code of 200.
        """
        query = Q(users=request.user) | Q(owner=request.user)

        if pk:
            query = query & Q(pk=pk)
            project = Project.objects.get(query)
            serialized = ProjectSerializer(project)
            return Response(serialized.data, status=status.HTTP_200_OK)
        else:
            all_projects = Project.objects.filter(query)
            serialized_projects = ProjectSerializer(all_projects, many=True)

            if serialized_projects.data:
                return Response({
                    "projects": serialized_projects.data, 
                    "message": "Projects found"
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "message": "No projects found"
                }, status=status.HTTP_200_OK)