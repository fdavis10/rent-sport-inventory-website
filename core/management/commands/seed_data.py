from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from inventory.models import Category, Equipment
from rentals.models import Rental, RentalItem, Review
from decimal import Decimal
from datetime import date, timedelta
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    def handle(self, *args, **kwargs):
        self.stdout.write(
            self.style.HTTP_INFO(
                '\n' + '='*50 + '\n'
                'Начинаем заполнение базы данных...\n'
                '='*50
            )
        )

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
                # Обновляем роль у существующих пользователей (на случай миграции)
                user.role = user_data['role']
                user.save()  # Метод save() автоматически установит is_staff и is_superuser
                self.stdout.write(
                    self.style.WARNING(
                        f'  ⚠ {user.get_role_display()}: {username} уже существует '
                        f'(обновлены права: is_staff={user.is_staff}, is_superuser={user.is_superuser})'
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Создано пользователей: {len(created_users)}')
        )

        # ========================================
        # 2. СОЗДАНИЕ КАТЕГОРИЙ
        # ========================================

        self.stdout.write(self.style.WARNING('\n[2/5] Создание категорий...'))

        categories_data = [
            {
                'name': 'Горные лыжи',
                'slug': 'gornye-lyzhi',
                'description': 'Лыжи для катания по горным склонам различной сложности'
            },
            {
                'name': 'Сноуборды',
                'slug': 'snowboards',
                'description': 'Доски для катания по снегу'
            },
            {
                'name': 'Коньки',
                'slug': 'konki',
                'description': 'Коньки для катания на льду'
            },
            {
                'name': 'Санки и тюбинги',
                'slug': 'sanki-tyubingi',
                'description': 'Средства для катания с горок'
            },
            {
                'name': 'Аксессуары',
                'slug': 'accessories',
                'description': 'Дополнительное снаряжение и экипировка'
            },
        ]

        created_categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            if created:
                created_categories.append(category)
                self.stdout.write(self.style.SUCCESS(f'  ✓ {category.name}'))

        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Создано категорий: {len(created_categories)}')
        )

        # Получаем все категории для создания инвентаря
        categories = list(Category.objects.all())

        # ========================================
        # 3. СОЗДАНИЕ ИНВЕНТАРЯ
        # ========================================

        self.stdout.write(self.style.WARNING('\n[3/5] Создание инвентаря...'))

        equipment_data = [
            # Горные лыжи
            {
                'name': 'Горные лыжи Head Kore 93',
                'slug': 'gornye-lyzhi-head-kore-93',
                'category': categories[0],
                'description': 'Универсальные лыжи для фрирайда и трассового катания. Отлично подходят для различных снежных условий.',
                'brand': 'Head',
                'model': 'Kore 93',
                'size': '170 см',
                'condition': Equipment.Condition.EXCELLENT,
                'price_per_day': Decimal('1500.00'),
                'quantity_total': 5,
                'quantity_available': 5,
            },
            {
                'name': 'Горные лыжи Atomic Vantage 97 Ti',
                'slug': 'gornye-lyzhi-atomic-vantage-97',
                'category': categories[0],
                'description': 'All-mountain лыжи для продвинутых райдеров. Стабильность на высоких скоростях.',
                'brand': 'Atomic',
                'model': 'Vantage 97 Ti',
                'size': '175 см',
                'condition': Equipment.Condition.EXCELLENT,
                'price_per_day': Decimal('1600.00'),
                'quantity_total': 4,
                'quantity_available': 4,
            },
            {
                'name': 'Горные лыжи Salomon QST 92',
                'slug': 'gornye-lyzhi-salomon-qst-92',
                'category': categories[0],
                'description': 'Легкие и маневренные лыжи для целинного катания.',
                'brand': 'Salomon',
                'model': 'QST 92',
                'size': '165 см',
                'condition': Equipment.Condition.GOOD,
                'price_per_day': Decimal('1400.00'),
                'quantity_total': 6,
                'quantity_available': 6,
            },

            # Сноуборды
            {
                'name': 'Сноуборд Burton Custom',
                'slug': 'snowboard-burton-custom',
                'category': categories[1],
                'description': 'Легендарный all-mountain сноуборд. Подходит для любого стиля катания.',
                'brand': 'Burton',
                'model': 'Custom',
                'size': '156 см',
                'condition': Equipment.Condition.EXCELLENT,
                'price_per_day': Decimal('1600.00'),
                'quantity_total': 4,
                'quantity_available': 4,
            },
            {
                'name': 'Сноуборд Ride Warpig',
                'slug': 'snowboard-ride-warpig',
                'category': categories[1],
                'description': 'Широкий сноуборд для пухляка и парка. Игривый и маневренный.',
                'brand': 'Ride',
                'model': 'Warpig',
                'size': '148 см',
                'condition': Equipment.Condition.EXCELLENT,
                'price_per_day': Decimal('1700.00'),
                'quantity_total': 3,
                'quantity_available': 3,
            },
            {
                'name': 'Сноуборд K2 Manifest',
                'slug': 'snowboard-k2-manifest',
                'category': categories[1],
                'description': 'Стабильный фрирайд сноуборд для больших гор.',
                'brand': 'K2',
                'model': 'Manifest',
                'size': '160 см',
                'condition': Equipment.Condition.GOOD,
                'price_per_day': Decimal('1500.00'),
                'quantity_total': 5,
                'quantity_available': 5,
            },

            # Коньки
            {
                'name': 'Коньки хоккейные Bauer Vapor X2.7',
                'slug': 'konki-bauer-vapor-x27',
                'category': categories[2],
                'description': 'Профессиональные хоккейные коньки с отличной поддержкой.',
                'brand': 'Bauer',
                'model': 'Vapor X2.7',
                'size': '42',
                'condition': Equipment.Condition.EXCELLENT,
                'price_per_day': Decimal('500.00'),
                'quantity_total': 10,
                'quantity_available': 10,
            },
            {
                'name': 'Коньки фигурные Graf Edmonton',
                'slug': 'konki-graf-edmonton',
                'category': categories[2],
                'description': 'Качественные фигурные коньки для начинающих и любителей.',
                'brand': 'Graf',
                'model': 'Edmonton',
                'size': '38',
                'condition': Equipment.Condition.GOOD,
                'price_per_day': Decimal('400.00'),
                'quantity_total': 8,
                'quantity_available': 8,
            },
            {
                'name': 'Коньки хоккейные CCM Tacks AS-V',
                'slug': 'konki-ccm-tacks-asv',
                'category': categories[2],
                'description': 'Удобные хоккейные коньки с анатомической посадкой.',
                'brand': 'CCM',
                'model': 'Tacks AS-V',
                'size': '44',
                'condition': Equipment.Condition.EXCELLENT,
                'price_per_day': Decimal('550.00'),
                'quantity_total': 6,
                'quantity_available': 6,
            },

            # Санки и тюбинги
            {
                'name': 'Тюбинг 100 см',
                'slug': 'tyubing-100',
                'category': categories[3],
                'description': 'Надувные санки-ватрушка диаметром 100 см. Максимальная нагрузка 120 кг.',
                'brand': 'Snowtube',
                'model': 'Classic 100',
                'size': '100 см',
                'condition': Equipment.Condition.EXCELLENT,
                'price_per_day': Decimal('300.00'),
                'quantity_total': 15,
                'quantity_available': 15,
            },
            {
                'name': 'Тюбинг 120 см',
                'slug': 'tyubing-120',
                'category': categories[3],
                'description': 'Надувные санки большого диаметра. Подходит для взрослых.',
                'brand': 'Snowtube',
                'model': 'Classic 120',
                'size': '120 см',
                'condition': Equipment.Condition.GOOD,
                'price_per_day': Decimal('350.00'),
                'quantity_total': 12,
                'quantity_available': 12,
            },
            {
                'name': 'Санки детские',
                'slug': 'sanki-detskie',
                'category': categories[3],
                'description': 'Классические деревянные санки для детей.',
                'brand': 'Русские Санки',
                'model': 'Классик',
                'size': 'Детские',
                'condition': Equipment.Condition.SATISFACTORY,
                'price_per_day': Decimal('200.00'),
                'quantity_total': 20,
                'quantity_available': 20,
            },

            # Аксессуары
            {
                'name': 'Шлем горнолыжный',
                'slug': 'shlem-gornolyzhnyi',
                'category': categories[4],
                'description': 'Защитный шлем для горных лыж и сноуборда.',
                'brand': 'Smith',
                'model': 'Vantage MIPS',
                'size': 'M (55-59 см)',
                'condition': Equipment.Condition.EXCELLENT,
                'price_per_day': Decimal('200.00'),
                'quantity_total': 25,
                'quantity_available': 25,
            },
            {
                'name': 'Маска горнолыжная',
                'slug': 'maska-gornolyzhnaya',
                'category': categories[4],
                'description': 'Маска с двойными линзами и защитой от запотевания.',
                'brand': 'Oakley',
                'model': 'Flight Deck',
                'size': 'Универсальный',
                'condition': Equipment.Condition.EXCELLENT,
                'price_per_day': Decimal('150.00'),
                'quantity_total': 20,
                'quantity_available': 20,
            },
            {
                'name': 'Палки лыжные',
                'slug': 'palki-lyzhnye',
                'category': categories[4],
                'description': 'Алюминиевые телескопические палки для горных лыж.',
                'brand': 'Leki',
                'model': 'Alpine',
                'size': '110-135 см (регулируемые)',
                'condition': Equipment.Condition.GOOD,
                'price_per_day': Decimal('100.00'),
                'quantity_total': 30,
                'quantity_available': 30,
            },
        ]

        created_equipment = []
        for eq_data in equipment_data:
            equipment, created = Equipment.objects.get_or_create(
                slug=eq_data['slug'],
                defaults=eq_data
            )
            if created:
                created_equipment.append(equipment)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  ✓ {equipment.name} ({equipment.category.name}) - '
                        f'{equipment.price_per_day}₽/день, {equipment.quantity_total} шт.'
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Создано единиц инвентаря: {len(created_equipment)}')
        )

        # ========================================
        # 4. СОЗДАНИЕ ТЕСТОВЫХ ЗАКАЗОВ
        # ========================================

        self.stdout.write(self.style.WARNING('\n[4/5] Создание тестовых заказов...'))

        # Получаем клиентов и менеджера
        clients = User.objects.filter(role=User.Role.CLIENT)
        manager = User.objects.filter(role=User.Role.MANAGER).first()

        if not clients.exists():
            self.stdout.write(
                self.style.WARNING('  ⚠ Нет клиентов для создания заказов')
            )
        else:
            created_rentals = []
            
            # Завершенный заказ (для примера с отзывами)
            rental1 = Rental.objects.create(
                user=clients[0],
                status=Rental.Status.COMPLETED,
                start_date=date.today() - timedelta(days=10),
                end_date=date.today() - timedelta(days=3),
                total_price=Decimal('10500.00'),
                comment='Отличный инвентарь!',
                confirmed_by=manager,
            )
            
            # Добавляем позиции в заказ
            equipment1 = Equipment.objects.get(slug='gornye-lyzhi-head-kore-93')
            RentalItem.objects.create(
                rental=rental1,
                equipment=equipment1,
                quantity=1,
                price_per_day=equipment1.price_per_day,
                days=7,
                subtotal=Decimal('10500.00')
            )
            created_rentals.append(rental1)
            self.stdout.write(
                self.style.SUCCESS(
                    f'  ✓ Заказ #{rental1.id} (COMPLETED) для {rental1.user.username}'
                )
            )

            # Активный заказ
            if len(clients) > 1:
                rental2 = Rental.objects.create(
                    user=clients[1],
                    status=Rental.Status.ACTIVE,
                    start_date=date.today() - timedelta(days=2),
                    end_date=date.today() + timedelta(days=3),
                    total_price=Decimal('8000.00'),
                    confirmed_by=manager,
                )
                
                equipment2 = Equipment.objects.get(slug='snowboard-burton-custom')
                RentalItem.objects.create(
                    rental=rental2,
                    equipment=equipment2,
                    quantity=1,
                    price_per_day=equipment2.price_per_day,
                    days=5,
                    subtotal=Decimal('8000.00')
                )
                created_rentals.append(rental2)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  ✓ Заказ #{rental2.id} (ACTIVE) для {rental2.user.username}'
                    )
                )

            # Ожидающий подтверждения заказ
            if len(clients) > 2:
                rental3 = Rental.objects.create(
                    user=clients[2],
                    status=Rental.Status.PENDING,
                    start_date=date.today() + timedelta(days=5),
                    end_date=date.today() + timedelta(days=12),
                    total_price=Decimal('3500.00'),
                )
                
                equipment3 = Equipment.objects.get(slug='konki-bauer-vapor-x27')
                RentalItem.objects.create(
                    rental=rental3,
                    equipment=equipment3,
                    quantity=1,
                    price_per_day=equipment3.price_per_day,
                    days=7,
                    subtotal=Decimal('3500.00')
                )
                created_rentals.append(rental3)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  ✓ Заказ #{rental3.id} (PENDING) для {rental3.user.username}'
                    )
                )

            self.stdout.write(
                self.style.SUCCESS(f'\n✅ Создано заказов: {len(created_rentals)}')
            )

        # ========================================
        # 5. СОЗДАНИЕ ТЕСТОВЫХ ОТЗЫВОВ
        # ========================================

        self.stdout.write(self.style.WARNING('\n[5/5] Создание тестовых отзывов...'))

        created_reviews = []
        
        # Отзыв от первого клиента на завершенный заказ
        if clients.exists():
            completed_rentals = Rental.objects.filter(
                user=clients[0],
                status=Rental.Status.COMPLETED
            )
            
            if completed_rentals.exists():
                rental = completed_rentals.first()
                rental_items = RentalItem.objects.filter(rental=rental)
                
                for item in rental_items:
                    review, created = Review.objects.get_or_create(
                        user=clients[0],
                        equipment=item.equipment,
                        rental=rental,
                        defaults={
                            'rating': 5,
                            'comment': 'Отличное качество! Лыжи в идеальном состоянии, очень понравилось кататься.'
                        }
                    )
                    if created:
                        created_reviews.append(review)
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'  ✓ Отзыв от {review.user.username} '
                                f'на {review.equipment.name} (⭐ {review.rating})'
                            )
                        )

        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Создано отзывов: {len(created_reviews)}')
        )

        # ========================================
        # ИТОГИ
        # ========================================

        self.stdout.write(
            self.style.HTTP_INFO(
                '\n' + '='*50 + '\n'
                'ЗАПОЛНЕНИЕ ЗАВЕРШЕНО!\n'
                '='*50 + '\n'
                f'Пользователи:  {User.objects.count()}\n'
                f'Категории:     {Category.objects.count()}\n'
                f'Инвентарь:     {Equipment.objects.count()}\n'
                f'Заказы:        {Rental.objects.count()}\n'
                f'Отзывы:        {Review.objects.count()}\n'
                '='*50 + '\n'
                'Тестовые пользователи:\n'
                '  Клиент:   ivan_petrov / Client123\n'
                '  Менеджер: manager / Manager123 (доступ к админке ✓)\n'
                '  Админ:    admin / Admin123 (полный доступ ✓)\n'
                '='*50
            )
        )