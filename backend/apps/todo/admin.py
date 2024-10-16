from django.contrib import admin
from . import models
from unfold.admin import ModelAdmin


@admin.register(models.Todo)
class TodoAdmin(ModelAdmin):
    list_display = ["title", "description", "completed", "created_at"]
    search_fields = ["title", "description"]
    list_filter = ["completed", "created_at"]
    ordering = ["-created_at"]

@admin.register(models.Project)
class ProjectAdmin(ModelAdmin):
    list_display = ["title", "completed", "owner"]
    search_fields = ["title"]
    list_filter = ["completed"]
    ordering = ["-completed"]
    fieldsets = (
        ("Project Details", {
            "fields": ("title", "image", "url", "completed", "owner")
        }),
        ("Project Timeline", {
            "fields": ("date_completed",),
            "classes": ("collapse",),
        }),
        ("Project Members", {
            "fields": ("users",),
            "classes": ("collapse",),
        }),
    )

@admin.register(models.Task)
class TaskAdmin(ModelAdmin):
    list_display = ["title", "description", "completed", "project"]
    search_fields = ["title", "project"]
    list_filter = ["completed"]
    ordering = ["-project"]

    fieldsets = (
        ("Task Details", {
            "fields": ("title", "project", "description", "completed",),
            "classes": ("collapse",),
        }),
    )

@admin.register(models.SharedTask)
class SharedTaskAdmin(ModelAdmin):
    list_display = ["owner", "task", "comment"]
    search_fields = ["owner", "to_user", "task"]
    list_filter = ["owner"]
    ordering = ["-owner"]
    fieldsets = (
        ("Shared Task Details", {
            "fields": ("owner", "to_user", "task", "comment"),
            "classes": ("collapse",),
        }),
    )

@admin.register(models.SharedTodo)
class SharedTodoAdmin(ModelAdmin):
    list_display = ["todo"]
    search_fields = ["to_user", "todo"]

    fieldsets = (
        ("Shared Todo Details", {
            "fields": ("todo", "to_user",),
            "classes": ("collapse",),
        }),

    )