from rest_framework import serializers
from .models import Project, Task


class TaskSerializer(serializers.ModelSerializer):
    # campos legíveis (ex: "Alta" em vez de "high")
    priority_display = serializers.CharField(source="get_priority_display", read_only=True)
    status_display   = serializers.CharField(source="get_status_display",   read_only=True)

    class Meta:
        model  = Task
        fields = [
            "id", "title", "description",
            "priority", "priority_display",
            "status",   "status_display",
            "due_date", "created_at", "updated_at",
            "project",  # aceita o ID na escrita
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_project(self, project):
        """Garante que o usuário só associa tarefas a projetos seus."""
        request = self.context["request"]
        if project.owner != request.user:
            raise serializers.ValidationError("Projeto não encontrado.")
        return project


class ProjectSerializer(serializers.ModelSerializer):
    tasks      = TaskSerializer(many=True, read_only=True)  # tarefas aninhadas
    task_count = serializers.IntegerField(source="tasks.count", read_only=True)

    class Meta:
        model  = Project
        fields = ["id", "name", "description", "created_at", "task_count", "tasks"]
        read_only_fields = ["id", "created_at"]