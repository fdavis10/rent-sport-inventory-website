from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
import os

User = get_user_model()


class Command(BaseCommand):
    help = 'Создает трёх пользователей (ADMIN, MANAGER, CLIENT) если их нет'

    def handle(self, *args, **options):
        users_data = [
            {
                'username': os.getenv('ADMIN_USERNAME', 'admin_test_local'),
                'email': os.getenv('ADMIN_EMAIL', 'adminlocal@sportarenda.ru'),
                'password': os.getenv('ADMIN_PASSWORD', 'admin_test_local_password_2504'),
                'first_name': os.getenv('ADMIN_FIRSTNAME', 'Владимир'),
                'last_name': os.getenv('ADMIN_LASTNAME', 'Тельный'),
                'role': User.Role.ADMIN,
            },
            {
                'username': os.getenv('MANAGER_USERNAME', 'manager_test_local'),
                'email': os.getenv('MANAGER_EMAIL', 'managerlocal@sportarenda.ru'),
                'password': os.getenv('MANAGER_PASSWORD', 'manager_test_local_password_2504'),
                'first_name': os.getenv('MANAGER_FIRSTNAME', 'Эвелина'),
                'last_name': os.getenv('MANAGER_LASTNAME', 'Шкляева'),
                'role': User.Role.MANAGER,
            },
            {
                'username': os.getenv('CLIENT_USERNAME', 'client_test_local'),
                'email': os.getenv('CLIENT_EMAIL', 'clientlocal@example.com'),
                'password': os.getenv('CLIENT_PASSWORD', 'client_test_local_password_2504'),
                'first_name': os.getenv('CLIENT_FIRSTNAME', 'Кирилл'),
                'last_name': os.getenv('CLIENT_LASTNAME', 'Зубило'),
                'role': User.Role.CLIENT,
            },
        ]
        
        created_count = 0
        existing_count = 0
        
        self.stdout.write(
            self.style.SUCCESS(
                '\n' + '='*60 + '\n'
                '🚀 СОЗДАНИЕ ПОЛЬЗОВАТЕЛЕЙ\n'
                '='*60
            )
        )
        
        for user_data in users_data:
            username = user_data['username']
            role = user_data['role']
            
            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(
                        f'⚠️  Пользователь "{username}" ({role}) уже существует'
                    )
                )
                existing_count += 1
                continue
            
            try:
                password = user_data.pop('password')
                role = user_data.pop('role')
                
                user = User.objects.create_user(
                    password=password,
                    **user_data
                )
                
                user.role = role
                user.save()
                
                created_count += 1
                
                role_emoji = {
                    User.Role.ADMIN: '👑',
                    User.Role.MANAGER: '👔',
                    User.Role.CLIENT: '👤',
                }
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'\n✅ {role_emoji[role]} {role} создан:\n'
                        f'   Логин:    {user.username}\n'
                        f'   Email:    {user.email}\n'
                        f'   Пароль:   {password}\n'
                        f'   Имя:      {user.get_full_name()}\n'
                        f'   is_staff: {user.is_staff}\n'
                        f'   is_superuser: {user.is_superuser}'
                    )
                )
                
            except IntegrityError as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Ошибка создания {username}: {e}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Неожиданная ошибка для {username}: {e}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                '\n' + '='*60 + '\n'
                f'📊 ИТОГО:\n'
                f'   Создано:       {created_count}\n'
                f'   Уже существует: {existing_count}\n'
                f'   Всего:         {created_count + existing_count}\n'
                '='*60 + '\n'
                '🔗 URL для входа:\n'
                '   Главная:  http://localhost:8000/\n'
                '   Админка:  http://localhost:8000/myadmin/\n'
                '='*60
            )
        )