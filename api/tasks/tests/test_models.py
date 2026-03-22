from django.test import TestCase
from django.contrib.auth import get_user_model
from tasks.models import Project, Task

User = get_user_model()


class ProjectModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com", name="User", password="pass123"
        )
        self.project = Project.objects.create(
            owner=self.user,
            name="Meu Projeto",
        )

    def test_project_str(self):
        """__str__ deve retornar nome e email do dono."""
        self.assertEqual(str(self.project), "Meu Projeto (user@example.com)")

    def test_project_owner(self):
        """Projeto deve estar associado ao usuário correto."""
        self.assertEqual(self.project.owner, self.user)

    def test_deleting_user_deletes_projects(self):
        """Deletar usuário deve deletar seus projetos (CASCADE)."""
        self.user.delete()
        self.assertEqual(Project.objects.count(), 0)


class TaskModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com", name="User", password="pass123"
        )
        self.project = Project.objects.create(owner=self.user, name="Projeto")
        self.task = Task.objects.create(
            project=self.project,
            title="Minha Tarefa",
            priority=Task.Priority.HIGH,
            status=Task.Status.TODO,
        )

    def test_task_str(self):
        """__str__ deve retornar título e status legível."""
        self.assertEqual(str(self.task), "Minha Tarefa [A fazer]")

    def test_task_default_priority(self):
        """Prioridade padrão deve ser medium."""
        task = Task.objects.create(project=self.project, title="Sem prioridade")
        self.assertEqual(task.priority, Task.Priority.MEDIUM)

    def test_task_default_status(self):
        """Status padrão deve ser todo."""
        task = Task.objects.create(project=self.project, title="Sem status")
        self.assertEqual(task.status, Task.Status.TODO)

    def test_deleting_project_deletes_tasks(self):
        """Deletar projeto deve deletar suas tarefas (CASCADE)."""
        self.project.delete()
        self.assertEqual(Task.objects.count(), 0)