from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import TodoSerializer, ProjectSerializer
from ..models import Todo, Project
from django.db.models import Q



class TodosList(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = TodoSerializer

    def get(self, request):
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
        user_todos = Todo.objects.filter(owner=request.user)
        serialized_todos = TodoSerializer(user_todos, many=True)
        return Response(serialized_todos.data, status=status.HTTP_200_OK)



class TodosDetail(APIView):
    def get(self, request, pk):
        """
        Retrieves a specific todo item by its primary key for the current user.

        Args:
            request (HttpRequest): The request object containing user details.
            pk (int): The primary key of the todo item to be retrieved.

        Returns:
            Response: A Response object with the serialized todo item data and a status code of 200,
                    or a status code of 404 if the todo item does not exist.
        """
        try:
            todo = Todo.objects.get(owner=request.user, pk=pk)
            serializer = TodoSerializer(todo)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    
    def put(self, request, pk):
        """
        Updates a todo item identified by the pk parameter.

        Args:
            request: The request object
            pk: The id of the todo item to update

        Returns:
            Response: A response object containing the updated todo item data and a status code of 200
        """
        try:
            todo = Todo.objects.get(owner=request.user, pk=pk)
            serializer = TodoSerializer(todo, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
   
   
    def delete(self, request, pk):
        """
        Deletes a todo item identified by the pk parameter.

        Args:
            request (Request): The request object
            pk (int): The id of the todo item to delete

        Returns:
            Response: A response object with a status of 204 or 404
        """
        try:
            todo = Todo.objects.get(owner=request.user, pk=pk)
            todo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    

    def complete(self, request, pk):
        """
        Completes a todo item.

        Args:
            request (HttpRequest): The request object.
            pk (int): The primary key of the todo item to be completed.

        Returns:
            Response: A Response object containing the serialized data of the
                completed todo item and a status code of 200.

        Raises:
            Http404: If the requested todo item does not exist.
        """

        try:
            todo = Todo.objects.get(owner=request.user, pk=pk)
            todo.completed = not todo.completed
            todo.save()
            serializer = TodoSerializer(todo)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Todo.DoesNotExist:
        
            return Response(status=status.HTTP_404_NOT_FOUND)
        


class ProjectsList(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = ProjectSerializer

    def get(self, request):
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
