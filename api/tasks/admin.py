from django.contrib import admin

from django.contrib import admin
from .models import Project, Task


class TaskInline(admin.TabularInline):
    """Mostra as tarefas dentro da tela do projeto no admin."""
    model = Task
    extra = 0
    fields = ["title", "status", "priority", "due_date"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", "created_at"]
    search_fields = ["name", "owner__email"]
    inlines = [TaskInline]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "project", "status", "priority", "due_date"]
    list_filter = ["status", "priority"]
    search_fields = ["title", "project__name"]