from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
import os

User = get_user_model()


class Command(BaseCommand):
    help = 'Создает суперпользователя если его нет'

    def handle(self, *args, **options):

        username = os.getenv('DJANGO_SUPERUSER_USERNAME')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD')
        first_name = os.getenv('DJANGO_SUPERUSER_FIRSTNAME')
        last_name = os.getenv('DJANGO_SUPERUSER_LASTNAME')
        

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(
                    f'⚠️  Суперпользователь "{username}" уже существует'
                )
            )
            return
        

        try:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            

            user.role = User.Role.ADMIN
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    '\n' + '='*50 + '\n'
                    '✅ СУПЕРПОЛЬЗОВАТЕЛЬ СОЗДАН!\n'
                    '='*50 + '\n'
                    f'Логин:    {username}\n'
                    f'Email:    {email}\n'
                    f'Пароль:   {password}\n'
                    f'Имя:      {first_name} {last_name}\n'
                    f'Роль:     {user.get_role_display()}\n'
                    '='*50 + '\n'
                    'Админка: http://localhost:8000/admin/\n'
                    '='*50
                )
            )
            
        except IntegrityError as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Ошибка создания: {e}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Неожиданная ошибка: {e}')
            )