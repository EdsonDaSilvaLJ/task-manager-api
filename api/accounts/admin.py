from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering        = ["email"]
    list_display    = ["email", "name", "is_staff", "is_active"]
    search_fields   = ["email", "name"]

    # campos exibidos ao editar um usuário
    fieldsets = (
        (None,            {"fields": ("email", "password")}),
        ("Dados pessoais", {"fields": ("name",)}),
        ("Permissões",    {"fields": ("is_active", "is_staff", "is_superuser", "groups")}),
    )
    # campos exibidos ao criar um usuário pelo admin
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields":  ("email", "name", "password1", "password2"),
        }),
    )