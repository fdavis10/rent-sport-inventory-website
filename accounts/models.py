from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        CLIENT = 'CLIENT', 'Клиент'
        MANAGER = 'MANAGER', 'Менеджер'
        ADMIN = 'ADMIN', 'Администратор'

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.CLIENT,
        verbose_name='Роль'
    )
    
    phone_number = models.CharField(
        max_length=17,
        blank=True,
        null=True,
        verbose_name='Телефон'
    )
    
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name='Адрес'
    )
    
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата рождения'
    )
    
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']

    def str(self):
        return f'{self.get_full_name()} ({self.get_role_display()})'
    
    def save(self, *args, **kwargs):
        if self.role in [self.Role.MANAGER, self.Role.ADMIN]:
            self.is_staff = True
        else:
            self.is_staff = False
        
        if self.role == self.Role.ADMIN:
            self.is_superuser = True
        else:
            self.is_superuser = False
        
        super().save(*args, **kwargs)