from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    """
    custom user models with roles

    """

    class Role(models.TextChoices):
        CLIENT = 'CLIENT', 'Клиент'
        MANAGER = 'MANAGER', 'Менеджер'
        ADMIN = 'ADMIN', 'Администратор'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CLIENT,
        verbose_name='Роль пользователя',
    )

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Номер телефона должен быть введен в формате: '+999999999'. До 15 цифр разрешено.",
    )

    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        verbose_name='Номер телефона',
    )

    address = models.CharField(
        blank=True,
        verbose_name='Адрес',
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата рождения',
    )

    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        verbose_name='Аватар',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
    
    # methods to check user roles

    @property
    def is_client(self):
        return self.role == self.Role.CLIENT
    
    @property
    def is_manager(self):
        return self.role == self.Role.MANAGER
    
    @property
    def is_admind(self):
        return self.role == self.Role.ADMIN