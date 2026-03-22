from django.db import models
from django.conf import settings

class Project(models.Model):
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
  name = models.CharField(max_length=150)
  description = models.TextField(blank=True)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ['-created_at'] #ordena do mais recente pro mais antigo
    verbose_name = 'Projeto' #verbose name é o nome que aparece no admin, se n definir ele pega o nome da classe, se definir ele pega o nome definido aqui
    verbose_name_plural = 'Projetos' #verbose name plural é o nome que aparece no admin quando tem mais de um, se n definir ele pega o nome da classe + 's', se definir ele pega o nome definido aqui

  def __str__(self):
    return f"{self.name} ({self.owner.email})"

class Task(models.Model): 
  class Priority(models.TextChoices):
    LOW = 'L', 'Baixa'
    MEDIUM = 'M', 'Média'
    HIGH = 'H', 'Alta'

  #vantagem de usar TextChoices é que ele já tem os métodos para pegar o valor e o label, além de ser mais fácil de ler
  #metodos de um TextChoices: .choices, .values, .labels, .get_label(value), .get_value(label)
  """vou explicar cada vantagem de choices:
  1. Ele já tem os métodos para pegar o valor e o label, além de ser mais fácil de ler. Por exemplo, se eu quiser pegar o label da prioridade baixa, eu posso usar Task.Priority.get_label(Task.Priority.LOW) e ele vai me retornar 'Baixa'. Se eu quiser pegar o valor da prioridade baixa, eu posso usar Task.Priority.get_value('Baixa') e ele vai me retornar 'L'.
  2. Ele já tem os métodos para pegar a lista de escolhas, o que facilita na hora de criar um campo de escolha no serializer. Por exemplo, se eu quiser criar um campo de escolha para a prioridade, eu posso usar serializers.ChoiceField(choices=Task.Priority.choices) e ele já vai me retornar a lista de escolhas no formato correto.
  3. Ele já tem os métodos para pegar o valor e o label, o que facilita na hora de criar um campo de escolha no serializer. Por exemplo, se eu quiser criar um campo de escolha para a prioridade, eu posso usar serializers.ChoiceField(choices=Task.Priority.choices) e ele já vai me retornar a lista de escolhas no formato correto, além de me permitir usar os métodos para pegar o valor e o label."""
  #usa o get_field_display próprio do django ja lidando com erros

  class Status(models.TextChoices):
    TODO = 'todo', 'A fazer'
    IN_PROGRESS = 'in_progress', 'Em Progresso'
    DONE = 'done', 'Feito'

  project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='tasks')
  title = models.CharField(max_length=200)
  description = models.TextField(blank=True)
  priority = models.CharField(
      max_length=10,
      choices=Priority.choices,
      default=Priority.MEDIUM
  )
  status = models.CharField(
      max_length=15,
      choices=Status.choices,
      default=Status.TODO
  )
  due_date = models.DateField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
      ordering = ["-created_at"]
      verbose_name = "Tarefa"
      verbose_name_plural = "Tarefas"

  def __str__(self):
      return f"{self.title} [{self.get_status_display()}]"