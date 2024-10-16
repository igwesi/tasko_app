from django.db import models
from apps.accounts.models import Account

class ProjectManager(models.Manager):
    def get_queryset(self):
        """
        Returns a queryset of projects that are not marked as completed.

        This method overrides the default `get_queryset` method of the `ProjectManager`
        to filter out projects that have been marked as completed.

        Returns:
            QuerySet: A queryset containing projects with `completed` set to `False`.
        """
        return super(ProjectManager, self).get_queryset().filter(completed=False)

class TaskManager(models.Manager):
    def get_queryset(self):
        return super(TaskManager, self).get_queryset().filter(completed=False)

class SharedTaskManager(models.Manager):
    def get_queryset(self):
        return super(SharedTaskManager, self).get_queryset().filter(task__completed=False)


class Project(models.Model):
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.URLField(default="https://via.placeholder.com/300", blank=True, null=True)
    url   = models.URLField(blank=True)

    users = models.ManyToManyField(Account, related_name='projects', blank=True)
    completed = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True)
    date_completed = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title
    
    def has_perms(self, user):
        """
        Checks if the given user has permission to view the project.

        Args:
            user: The user to check.

        Returns:
            bool: True if the user has permission to view the project, False otherwise.
        """
        if user != self.owner:
            return False
        return True
    
    def tasks(self):
        return Task.objects.filter(project=self)

    def shared_tasks(self):
        return SharedTask.objects.filter(task__project=self)

    def shared_users(self):
        """
        Retrieves a distinct list of user IDs who have been assigned shared tasks
        associated with the current project.
        Returns:
            QuerySet: A queryset of distinct user IDs.
        """
        return self.shared_tasks().values_list('to_user', flat=True).distinct()

    def shared_tasks_by_user(self, user):
        return self.shared_tasks().filter(to_user=user)

    def shared_tasks_by_users(self, users):
        """
        Retrieves shared tasks assigned to a list of users.
        """
        return self.shared_tasks().filter(to_user__in=users)
    
    def shared_tasks_by_date(self, start_date, end_date):
        return self.shared_tasks().filter(created_at__gte=start_date, created_at__lte=end_date)

    def shared_tasks_by_user_and_date(self, user, start_date, end_date):
        return self.shared_tasks_by_user(user).filter(created_at__gte=start_date, created_at__lte=end_date)


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    date_completed = models.DateField(blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks', blank=True, null=True)

    def __str__(self):
        return self.title


class SharedTask(models.Model):
    owner   = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='shared_tasks')
    to_user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='shared_tasks_by_user')

    task    = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='shared_tasks', blank=True, null=True)
    comment = models.CharField(blank=True, max_length=200)
    date_assigned = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.task.title
    
    def count(self):
        return SharedTask.objects.filter(owner=self.owner).count()


class Todo(models.Model):
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='todos')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def has_perms(self, user):
        if user != self.owner:
            return False
        return True
    
class SharedTodo(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name="shared_todo")
    to_user = models.ManyToManyField(Account, related_name="shared_users", blank=True, verbose_name="Members")
   
    def __str__(self):
        return self.todo.title