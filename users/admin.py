from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'departament', 'is_active', 'is_staff', 'date_joined')
    list_editable = ('is_active', 'departament')
    list_filter = ('is_active', 'is_staff', 'departament')
    search_fields = ('username', 'email', 'departament')
