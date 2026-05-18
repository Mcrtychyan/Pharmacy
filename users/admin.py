from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# from users.models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'full_name', 'phone', 'role', 'is_active')
    list_filter = ('role', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'full_name', 'phone')
    list_editable = ('role',)

    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('full_name', 'phone', 'role'),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {
            'fields': ('full_name', 'phone', 'role'),
        }),
    )