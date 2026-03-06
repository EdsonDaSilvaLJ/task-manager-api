from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
#Manager customizado.
#Manager -> normalize_email e get_by_natural_key
#Definir create_user and super_user
class UserManager(BaseUserManager):
  
  def create_user(self, email, password=None, **extra_fields):
    if not email:
      raise ValueError("Email is required.")
    email = self.normalize_email(email)
    user = self.model(email=email,**extra_fields)
    user.set_password(password) #Tenho que garantir qu emeu modelo tenha set_password que gere o hash no formato adequado algorítmo$reps$salts$passwords_hash
    user.save(using=self._db) #Garantir que vai ser no modelo instanciado
    return user #padrão do create
  
  def create_superuser(self, email, password, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)
    return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
  email = models.EmailField(unique=True) #Unique True porque vai ser username_field
  name = models.CharField(max_length=150)
  is_active = models.BooleanField(default=False) # create super user do meu manager usa
  is_staff = models.BooleanField(default=False) #create super user do meu manager usa
  created_at = models.DateTimeField(auto_now_add=True)

  objects = UserManager()

  #DEFINIR OS OBRIGATÓRIOS usernamefield pro authenticate que usa o AbstractBaseUser.get_by_natural_key
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['name'] #campos obrigatórios além do fieldusername e password

  def __str__(self):
    return self.email