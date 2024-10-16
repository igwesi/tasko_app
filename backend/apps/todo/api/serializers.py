from rest_framework import serializers
from ..models import Todo, SharedTodo, Project, ProjectManager, Task, SharedTask

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['title', 'description','completed', 'created_at']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description','completed', 'date_completed']
        read_only_fields = ['project']
        extra_kwargs = {'project': {'read_only': True}}


class SharedTodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedTodo
        fields = ['title', 'description','completed', 'created_at']
        read_only_fields = ['owner']
        extra_kwargs = {'owner': {'read_only': True}}

class SharedTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedTask
        fields = ['task', 'comment']
        read_only_fields = ['owner']
        extra_kwargs = {'owner': {'read_only': True}}


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'title', 
            'owner', 
            'members',
            'tasks', 
            'total_tasks', 
            'shared_tasks',
            'total_shared_tasks',
            'completed', 
        ]
        ordering = ['-created_at']

    tasks               = TaskSerializer(many=True, read_only=True)
    shared_tasks        = SharedTasksSerializer(many=True, read_only=True)
    owner               = serializers.SerializerMethodField()
    members             = serializers.SerializerMethodField()
    total_tasks         = serializers.SerializerMethodField()
    total_shared_tasks  = serializers.SerializerMethodField()
    

    def get_owner(self, obj):
        """
        Returns the email of the project's owner.
        """
        return obj.owner.email
    
    def get_total_tasks(self, obj):
        """
        Returns the total number of tasks in the project.
        """
        return obj.tasks.count()

    def get_total_shared_tasks(self, obj):
        """
        Returns the total number of shared tasks in the project.
        """
        return len(SharedTasksSerializer(obj.shared_tasks).data)
    
    def get_members(self, obj):
        """
        Returns a list of emails of the users in the project excluding the owner.
        """
        owner_email = obj.owner.email
        user_emails = [user.email for user in obj.users.all()]
        return [email for email in user_emails if email != owner_email]

    def create(self, validated_data):
        project_instance = Project.objects.create(**validated_data)
        return project_instance    

    def update(self, instance, validated_data):
        """
        Updates a project with the given validated data.
        """
        instance.title          = validated_data.get('title', instance.title)
        instance.description    = validated_data.get('description', instance.description)
        instance.completed      = validated_data.get('completed', instance.completed)
        instance.save()
        return instance
    
    def get_queryset(self):
        """
        Gets a queryset of projects that the current user owns.
        """
        return Project.objects.filter(owner=self.context['request'].user)
    
    def filter_queryset(self, queryset):
        filtered_queryset = super().filter_queryset(queryset)
        return filtered_queryset.filter(owner=self.context['request'].user)
