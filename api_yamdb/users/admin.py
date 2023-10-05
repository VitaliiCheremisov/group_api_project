from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

admin.site.empty_value_display = '-пусто-'


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role')
    search_fields = ('username', 'email', 'first_name', 'last_name',
                     'role', 'bio')
    list_filter = ('role',)
