from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'Пользователь'),
        ('pharmacist', 'Фармацевт'),
        ('admin', 'Администратор'),
    )

    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def is_pharmacist(self):
        return self.role == 'pharmacist'

    def is_admin_user(self):
        return self.role == 'admin' or self.is_superuser

    def can_manage_products(self):
        return self.role in ['pharmacist', 'admin'] or self.is_superuser

    def can_manage_users(self):
        return self.role == 'admin' or self.is_superuser

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'