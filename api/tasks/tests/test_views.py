from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from tasks.models import Project, Task

User = get_user_model()


class TaskTestCase(TestCase):
    """Classe base — dois usuários isolados para testar segurança."""

    def setUp(self):
        self.client  = APIClient()
        self.client2 = APIClient()

        self.user1 = User.objects.create_user(
            email="user1@example.com", name="User 1", password="pass123"
        )
        self.user2 = User.objects.create_user(
            email="user2@example.com", name="User 2", password="pass123"
        )

        # autentica cada client com seu usuário
        self._authenticate(self.client,  "user1@example.com")
        self._authenticate(self.client2, "user2@example.com")

        # projeto e tarefa do user1
        self.project = Project.objects.create(owner=self.user1, name="Projeto 1")
        self.task    = Task.objects.create(
            project=self.project,
            title="Tarefa 1",
            priority=Task.Priority.HIGH,
            status=Task.Status.TODO,
        )

    def _authenticate(self, client, email):
        response = client.post("/api/accounts/login/", {
            "email": email, "password": "pass123"
        })
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")


class ProjectTests(TaskTestCase):

    def test_list_only_own_projects(self):
        """User1 só deve ver seus próprios projetos."""
        Project.objects.create(owner=self.user2, name="Projeto do User2")
        response = self.client.get("/api/projects/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # só o projeto do user1

    def test_create_project(self):
        """Criação de projeto deve associar ao usuário logado automaticamente."""
        response = self.client.post("/api/projects/", {"name": "Novo Projeto"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.filter(owner=self.user1).count(), 2)

    def test_cannot_access_other_user_project(self):
        """User2 não pode ver detalhes do projeto do User1."""
        response = self.client2.get(f"/api/projects/{self.project.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_delete_other_user_project(self):
        """User2 não pode deletar projeto do User1."""
        response = self.client2.delete(f"/api/projects/{self.project.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TaskTests(TaskTestCase):

    def test_list_only_own_tasks(self):
        """User1 só deve ver tarefas dos seus próprios projetos."""
        project2 = Project.objects.create(owner=self.user2, name="P2")
        Task.objects.create(project=project2, title="Tarefa do User2")
        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_by_status(self):
        """Filtro por status deve retornar apenas tarefas correspondentes."""
        Task.objects.create(
            project=self.project, title="Tarefa Done", status=Task.Status.DONE
        )
        response = self.client.get("/api/tasks/?status=todo")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_by_priority(self):
        response = self.client.get(f"/api/tasks/?priority={Task.Priority.HIGH}")  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_cannot_create_task_in_other_user_project(self):
        """User2 não pode criar tarefa no projeto do User1."""
        response = self.client2.post("/api/tasks/", {
            "title":   "Invasão",
            "project": self.project.id,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)