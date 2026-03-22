from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

class AuthTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "email":     "test@example.com",
            "name":      "Test User",
            "password1": "testpass123",
            "password2": "testpass123",
        }
        self.user = User.objects.create_user(
            email=self.user_data["email"],
            name=self.user_data["name"],
            password=self.user_data["password1"],
        )

    def get_tokens(self):   # 👈 esse método precisa estar aqui
        response = self.client.post("/api/accounts/login/", {
            "email":    self.user_data["email"],
            "password": self.user_data["password1"],
        })
        return response.data


class RegisterTests(AuthTestCase):

    def test_register_success(self):
        data = {
            "email":     "new@example.com",
            "name":      "New User",
            "password1": "newpass123",   # 👈
            "password2": "newpass123",   # 👈
        }
        response = self.client.post("/api/accounts/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("email", response.data)

    def test_register_passwords_dont_match(self):
        data = {
            **self.user_data,
            "email":     "other@example.com",
            "password2": "wrongpass"     # password1 vem do user_data
        }
        response = self.client.post("/api/accounts/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class LoginTests(AuthTestCase):

    def test_login_success(self):
        """Login válido deve retornar access e refresh tokens."""
        tokens = self.get_tokens()
        self.assertIn("access",  tokens)
        self.assertIn("refresh", tokens)

    def test_login_wrong_password(self):
        """Senha errada deve retornar 401."""
        response = self.client.post("/api/accounts/login/", {
            "email":    self.user_data["email"],
            "password": "wrongpassword",
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_nonexistent_user(self):
        """Usuário inexistente deve retornar 401."""
        response = self.client.post("/api/accounts/login/", {
            "email":    "ghost@example.com",
            "password": "whatever",
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class MeTests(AuthTestCase):

    def test_me_authenticated(self):
        """Usuário autenticado deve ver seus próprios dados."""
        tokens = self.get_tokens()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        response = self.client.get("/api/accounts/me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user_data["email"])

    def test_me_unauthenticated(self):
        """Sem token deve retornar 401."""
        response = self.client.get("/api/accounts/me/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)