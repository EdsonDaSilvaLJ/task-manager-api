from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):

  #source pra quando passar pro validated_data passar como password
  password1 = serializers.CharField(source='password', min_length=8, max_length = 150, write_only=True) #Não posso voltar o hash inteiro no .data, volto só o token se for password, se for password1 é pra n dar erro
  password2 = serializers.CharField(max_length=150, write_only= True) #Pra n dar excessão

  class Meta:
    model = User
    fields = ('id', 'email', 'name', 'password1', 'password2')
    
    #validate é o passo antes do validated_data, se n definir ele apenas retorna attrs, se definir ai faz verificação entre os campos
  def validate(self, attrs):
    if attrs['password'] != attrs['password2']:
      raise serializers.ValidationError("Senhas tem que ser iguais")
    return attrs
    
  def create(self, validated_data):
    self.pop('password2') #retirar do validated_data
    return User.objects.create(**validated_data)
    
