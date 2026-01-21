# ========================================
# 1. СОЗДАНИЕ ПОЛЬЗОВАТЕЛЕЙ
# ========================================

self.stdout.write(self.style.WARNING('\n[1/5] Создание пользователей...'))

users_data = [
    {
        'username': 'ivan_petrov',
        'email': 'ivan.petrov@example.com',
        'password': 'Client123',
        'first_name': 'Иван',
        'last_name': 'Петров',
        'role': User.Role.CLIENT,
        'phone_number': '+7 (999) 111-11-11',
        'address': 'Москва, ул. Ленина, д. 1'
    },
    {
        'username': 'maria_ivanova',
        'email': 'maria.ivanova@example.com',
        'password': 'Client123',
        'first_name': 'Мария',
        'last_name': 'Иванова',
        'role': User.Role.CLIENT,
        'phone_number': '+7 (999) 222-22-22',
        'address': 'Москва, ул. Пушкина, д. 10'
    },
    {
        'username': 'alex_smirnov',
        'email': 'alex.smirnov@example.com',
        'password': 'Client123',
        'first_name': 'Алексей',
        'last_name': 'Смирнов',
        'role': User.Role.CLIENT,
        'phone_number': '+7 (999) 333-33-33',
    },
    {
        'username': 'manager',
        'email': 'manager@sportarenda.ru',
        'password': 'Manager123',
        'first_name': 'Менеджер',
        'last_name': 'Системы',
        'role': User.Role.MANAGER,
        'phone_number': '+7 (999) 123-45-68'
    },
    {
        'username': 'admin',
        'email': 'admin@sportarenda.ru',
        'password': 'Admin123',
        'first_name': 'Администратор',
        'last_name': 'Системы',
        'role': User.Role.ADMIN,
        'phone_number': '+7 (999) 123-45-67'
    }
]

created_users = []
for user_data in users_data:
    username = user_data['username']
    if not User.objects.filter(username=username).exists():
        password = user_data.pop('password')
        user = User.objects.create_user(
            password=password,
            **user_data
        )
        created_users.append(user)
        self.stdout.write(
            self.style.SUCCESS(
                f'  ✓ {user.get_role_display()}: {username} '
                f'(is_staff={user.is_staff}, is_superuser={user.is_superuser})'
            )
        )
    else:
        user = User.objects.get(username=username)
        user.role = user_data['role']
        user.save()  
        self.stdout.write(
            self.style.WARNING(
                f'  ⚠️ {user.get_role_display()}: {username} уже существует '
                f'(обновлены права: is_staff={user.is_staff}, is_superuser={user.is_superuser})'
            )
        )

self.stdout.write(
    self.style.SUCCESS(f'\n✅ Создано пользователей: {len(created_users)}')
)