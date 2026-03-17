from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """
    CRUD completo de projetos.
    O usuário só enxerga e manipula os próprios projetos.
    """
    serializer_class   = ProjectSerializer
    permission_classes = [IsAuthenticated]

    # filtros de busca por nome
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ["name"]
    ordering_fields  = ["name", "created_at"]

    def get_queryset(self):
        """Isolamento de dados: filtra pelo usuário logado."""
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """Injeta o owner automaticamente — o cliente não precisa enviar."""
        serializer.save(owner=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    """
    CRUD completo de tarefas com filtros por status, prioridade e projeto.
    """
    serializer_class   = TaskSerializer
    permission_classes = [IsAuthenticated]

    filter_backends  = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "priority", "project"]  # ?status=todo&priority=high
    search_fields    = ["title", "description"]            # ?search=bug
    ordering_fields  = ["due_date", "created_at", "priority"]

    def get_queryset(self):
        """Isolamento: só tarefas de projetos do usuário logado."""
        return Task.objects.filter(project__owner=self.request.user)