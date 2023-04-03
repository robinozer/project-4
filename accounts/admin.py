from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email')
    filter_horizontal = ('groups', 'user_permissions')


admin.site.register(User, CustomUserAdmin)
