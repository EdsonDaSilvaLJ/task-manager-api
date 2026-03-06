from django.shortcuts import render

from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    POST /api/accounts/register/
    Cria um novo usuário. Não exige autenticação.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]  # única rota pública


class MeView(generics.RetrieveUpdateAPIView):
    """
    GET  /api/accounts/me/  → retorna dados do usuário logado
    PATCH /api/accounts/me/ → atualiza nome, etc.
    """
    serializer_class=UserSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user  # sempre retorna o usuário do token


class LoginView(TokenObtainPairView):
    """
    POST /api/accounts/login/
    Recebe email + senha, retorna access + refresh token.
    Herda tudo do Simple JWT — só estamos nomeando a view.
    """
    permission_classes = [permissions.AllowAny]