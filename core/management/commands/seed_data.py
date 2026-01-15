from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from inventory.models import Category, Equipment
from rentals.models import Rental, RentalItem
from decimal import Decimal
from datetime import date, timedelta

User = get_user_model()


class Command(BaseCommand):
    help = 'Заполнение БД тестовыми данными'

    def handle(self, *args, **kwargs):
        self.stdout.write('Начало заполнения БД...')
        

        self.stdout.write('Очистка старых данных...')
        RentalItem.objects.all().delete()
        Rental.objects.all().delete()
        Equipment.objects.all().delete()
        Category.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        

        self.stdout.write('Создание пользователей...')
        

        client1 = User.objects.create_user(
            username='ivan_petrov',
            email='ivan@example.com',
            password='Client123',
            first_name='Иван',
            last_name='Петров',
            role=User.Role.CLIENT,
            phone_number='+79991234567',
            address='Москва, ул. Ленина, д. 10',
        )
        
        client2 = User.objects.create_user(
            username='maria_ivanova',
            email='maria@example.com',
            password='Client123',
            first_name='Мария',
            last_name='Иванова',
            role=User.Role.CLIENT,
            phone_number='+79991234568',
            address='Москва, ул. Пушкина, д. 5',
        )
        
        client3 = User.objects.create_user(
            username='alex_smirnov',
            email='alex@example.com',
            password='Client123',
            first_name='Александр',
            last_name='Смирнов',
            role=User.Role.CLIENT,
            phone_number='+79991234569',
        )
        
        manager = User.objects.create_user(
            username='manager',
            email='manager@example.com',
            password='Manager123',
            first_name='Ольга',
            last_name='Менеджерова',
            role=User.Role.MANAGER,
            phone_number='+79991234570',
        )


        admin_user = User.objects.create_user(
            username='administrator',
            email='administrator@example.com',
            password='Admin123',
            first_name='Дмитрий',
            last_name='Админов',
            role=User.Role.ADMIN,
            phone_number='+79991234571',
            is_staff=True,
        )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Создано 5 пользователей'))
        
        self.stdout.write('Создание категорий...')
        
        skis = Category.objects.create(
            name='Горные лыжи',
            slug='gornie-lyzhi',
            description='Горные лыжи для катания на склонах различной сложности',
            is_active=True,
        )
        
        snowboards = Category.objects.create(
            name='Сноуборды',
            slug='snowboards',
            description='Сноуборды для фристайла, фрирайда и карвинга',
            is_active=True,
        )
        
        skates = Category.objects.create(
            name='Коньки',
            slug='konki',
            description='Коньки для катания на льду',
            is_active=True,
        )
        
        sleds = Category.objects.create(
            name='Санки и тюбинги',
            slug='sanki-tubing',
            description='Санки, тюбинги для катания с горок',
            is_active=True,
        )
        
        accessories = Category.objects.create(
            name='Аксессуары',
            slug='accessories',
            description='Шлемы, защита, очки и другие аксессуары',
            is_active=True,
        )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Создано 5 категорий'))
        
        self.stdout.write('Создание инвентаря...')
        
        Equipment.objects.create(
            category=skis,
            name='Горные лыжи Head Kore 93',
            slug='head-kore-93-170',
            description='Универсальные горные лыжи для фрирайда и трассового катания. Отлично подходят для продвинутых лыжников.',
            brand='Head',
            model='Kore 93',
            size='170 см',
            condition=Equipment.Condition.EXCELLENT,
            price_per_day=Decimal('1500.00'),
            quantity_total=5,
            quantity_available=5,
        )
        
        Equipment.objects.create(
            category=skis,
            name='Горные лыжи Rossignol Experience 80',
            slug='rossignol-experience-80-160',
            description='Лыжи для начинающих и среднего уровня. Легкие и маневренные.',
            brand='Rossignol',
            model='Experience 80',
            size='160 см',
            condition=Equipment.Condition.GOOD,
            price_per_day=Decimal('1200.00'),
            quantity_total=8,
            quantity_available=8,
        )
        
        Equipment.objects.create(
            category=skis,
            name='Горные лыжи Atomic Vantage 90',
            slug='atomic-vantage-90-175',
            description='Профессиональные лыжи для экспертов. Стабильность на высоких скоростях.',
            brand='Atomic',
            model='Vantage 90',
            size='175 см',
            condition=Equipment.Condition.EXCELLENT,
            price_per_day=Decimal('1800.00'),
            quantity_total=3,
            quantity_available=3,
        )
        
        Equipment.objects.create(
            category=skis,
            name='Детские горные лыжи Salomon QST Max Jr',
            slug='salomon-qst-max-jr-130',
            description='Детские лыжи для начинающих лыжников 7-10 лет.',
            brand='Salomon',
            model='QST Max Jr',
            size='130 см',
            condition=Equipment.Condition.GOOD,
            price_per_day=Decimal('800.00'),
            quantity_total=10,
            quantity_available=10,
        )
        
        Equipment.objects.create(
            category=snowboards,
            name='Сноуборд Burton Custom',
            slug='burton-custom-156',
            description='Легендарный сноуборд для all-mountain катания. Подходит для любых условий.',
            brand='Burton',
            model='Custom',
            size='156 см',
            condition=Equipment.Condition.EXCELLENT,
            price_per_day=Decimal('1600.00'),
            quantity_total=6,
            quantity_available=6,
        )
        
        Equipment.objects.create(
            category=snowboards,
            name='Сноуборд Ride Warpig',
            slug='ride-warpig-148',
            description='Широкий сноуборд для фрирайда и паудера. Отличная проходимость.',
            brand='Ride',
            model='Warpig',
            size='148 см',
            condition=Equipment.Condition.GOOD,
            price_per_day=Decimal('1700.00'),
            quantity_total=4,
            quantity_available=4,
        )
        
        Equipment.objects.create(
            category=snowboards,
            name='Сноуборд Capita DOA',
            slug='capita-doa-154',
            description='Популярный сноуборд для парка и трасс. Игривый и отзывчивый.',
            brand='Capita',
            model='DOA',
            size='154 см',
            condition=Equipment.Condition.EXCELLENT,
            price_per_day=Decimal('1500.00'),
            quantity_total=5,
            quantity_available=5,
        )
        
        Equipment.objects.create(
            category=snowboards,
            name='Детский сноуборд Burton Chopper',
            slug='burton-chopper-120',
            description='Детский сноуборд для обучения. Мягкий и легкий.',
            brand='Burton',
            model='Chopper',
            size='120 см',
            condition=Equipment.Condition.GOOD,
            price_per_day=Decimal('900.00'),
            quantity_total=7,
            quantity_available=7,
        )
        
        Equipment.objects.create(
            category=skates,
            name='Хоккейные коньки Bauer Vapor X2.7',
            slug='bauer-vapor-x27-43',
            description='Хоккейные коньки для любителей. Удобная посадка.',
            brand='Bauer',
            model='Vapor X2.7',
            size='43',
            condition=Equipment.Condition.GOOD,
            price_per_day=Decimal('500.00'),
            quantity_total=12,
            quantity_available=12,
        )
        
        Equipment.objects.create(
            category=skates,
            name='Фигурные коньки Edea Overture',
            slug='edea-overture-38',
            description='Фигурные коньки для начинающих фигуристов.',
            brand='Edea',
            model='Overture',
            size='38',
            condition=Equipment.Condition.EXCELLENT,
            price_per_day=Decimal('600.00'),
            quantity_total=8,
            quantity_available=8,
        )
        
        Equipment.objects.create(
            category=skates,
            name='Прогулочные коньки Rollerblade Zetrablade',
            slug='rollerblade-zetrablade-42',
            description='Удобные коньки для прогулок на катке.',
            brand='Rollerblade',
            model='Zetrablade',
            size='42',
            condition=Equipment.Condition.GOOD,
            price_per_day=Decimal('400.00'),
            quantity_total=15,
            quantity_available=15,
        )
        
        Equipment.objects.create(
            category=sleds,
            name='Тюбинг классический 100см',
            slug='tubing-classic-100',
            description='Надувные санки-ватрушка для катания с горок.',
            brand='SnowShow',
            model='Classic',
            size='100 см',
            condition=Equipment.Condition.GOOD,
            price_per_day=Decimal('300.00'),
            quantity_total=20,
            quantity_available=20,
        )
        
        Equipment.objects.create(
            category=sleds,
            name='Санки-ледянка',
            slug='sledge-ledyanka',
            description='Пластиковая ледянка для катания с горок.',
            brand='Polar',
            model='Speed',
            size='Универсальный',
            condition=Equipment.Condition.SATISFACTORY,
            price_per_day=Decimal('150.00'),
            quantity_total=30,
            quantity_available=30,
        )
        
        Equipment.objects.create(
            category=accessories,
            name='Горнолыжный шлем POC Obex',
            slug='poc-obex-m',
            description='Защитный шлем для горных лыж и сноуборда.',
            brand='POC',
            model='Obex',
            size='M (55-58 см)',
            condition=Equipment.Condition.EXCELLENT,
            price_per_day=Decimal('400.00'),
            quantity_total=15,
            quantity_available=15,
        )
        
        Equipment.objects.create(
            category=accessories,
            name='Горнолыжные очки Oakley Flight Deck',
            slug='oakley-flight-deck',
            description='Профессиональные маска для катания. Широкий обзор.',
            brand='Oakley',
            model='Flight Deck',
            size='Универсальный',
            condition=Equipment.Condition.GOOD,
            price_per_day=Decimal('500.00'),
            quantity_total=10,
            quantity_available=10,
        )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Создано 16 единиц инвентаря'))
        
        self.stdout.write('Создание тестовых аренд...')
        
        rental1 = Rental.objects.create(
            user=client1,
            status=Rental.Status.COMPLETED,
            start_date=date.today() - timedelta(days=10),
            end_date=date.today() - timedelta(days=8),
            total_price=Decimal('3000.00'),
            confirmed_by=manager,
        )
        
        equipment1 = Equipment.objects.get(slug='head-kore-93-170')
        RentalItem.objects.create(
            rental=rental1,
            equipment=equipment1,
            quantity=1,
            price_per_day=equipment1.price_per_day,
            days=2,
        )
        
        rental2 = Rental.objects.create(
            user=client2,
            status=Rental.Status.ACTIVE,
            start_date=date.today() - timedelta(days=1),
            end_date=date.today() + timedelta(days=2),
            total_price=Decimal('4800.00'),
            confirmed_by=manager,
        )
        
        equipment2 = Equipment.objects.get(slug='burton-custom-156')
        RentalItem.objects.create(
            rental=rental2,
            equipment=equipment2,
            quantity=1,
            price_per_day=equipment2.price_per_day,
            days=3,
        )
        
        equipment2.quantity_available -= 1
        equipment2.save()
        
        rental3 = Rental.objects.create(
            user=client3,
            status=Rental.Status.PENDING,
            start_date=date.today() + timedelta(days=3),
            end_date=date.today() + timedelta(days=5),
            total_price=Decimal('2400.00'),
        )
        
        equipment3 = Equipment.objects.get(slug='bauer-vapor-x27-43')
        RentalItem.objects.create(
            rental=rental3,
            equipment=equipment3,
            quantity=2,
            price_per_day=equipment3.price_per_day,
            days=3,
        )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Создано 3 тестовые аренды'))
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена!'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(f'Пользователей: {User.objects.count()}')
        self.stdout.write(f'Категорий: {Category.objects.count()}')
        self.stdout.write(f'Единиц инвентаря: {Equipment.objects.count()}')
        self.stdout.write(f'Аренд: {Rental.objects.count()}')
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write('\nТестовые пользователи:')
        self.stdout.write('  Клиент: ivan_petrov / Client123')
        self.stdout.write('  Менеджер: manager / Manager123')
        self.stdout.write('  Админ: administrator / Admin123')