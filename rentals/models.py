from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from accounts.models import User
from inventory.models import Equipment


class Rental(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Ожидает подтверждения'
        CONFIRMED = 'CONFIRMED', 'Подтверждён'
        ACTIVE = 'ACTIVE', 'Активная аренда'
        COMPLETED = 'COMPLETED', 'Завершён'
        CANCELLED = 'CANCELLED', 'Отменён'
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='rentals',
        verbose_name='Клиент'
    )
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='Статус'
    )
    
    start_date = models.DateField(
        verbose_name='Дата начала аренды'
    )
    
    end_date = models.DateField(
        verbose_name='Дата окончания аренды'
    )
    
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Общая стоимость (руб.)'
    )
    
    comment = models.TextField(
        blank=True,
        verbose_name='Комментарий'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания заказа'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    
    confirmed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дата подтверждения'
    )
    
    confirmed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='confirmed_rentals',
        verbose_name='Подтвердил'
    )
    
    class Meta:
        verbose_name = 'Аренда'
        verbose_name_plural = 'Аренды'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Заказ №{self.pk} - {self.user.username} ({self.get_status_display()})"
    
    @property
    def duration_days(self):
        return (self.end_date - self.start_date).days + 1
    
    @property
    def is_active(self):
        return self.status == self.Status.ACTIVE
    
    @property
    def can_be_cancelled(self):
        return self.status in [self.Status.PENDING, self.Status.CONFIRMED]


class RentalItem(models.Model):
    rental = models.ForeignKey(
        Rental,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ'
    )
    
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.PROTECT,
        related_name='rental_items',
        verbose_name='Инвентарь'
    )
    
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name='Количество'
    )
    
    price_per_day = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Цена за день (руб.)'
    )
    
    days = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Количество дней'
    )
    
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Подытог (руб.)'
    )
    
    class Meta:
        verbose_name = 'Позиция аренды'
        verbose_name_plural = 'Позиции аренды'
        unique_together = ['rental', 'equipment']
    
    def __str__(self):
        return f"{self.equipment.name} x{self.quantity} ({self.days} дн.)"
    
    def save(self, *args, **kwargs):
        self.subtotal = self.price_per_day * self.quantity * self.days
        super().save(*args, **kwargs)


class Review(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Пользователь'
    )
    
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Инвентарь'
    )
    
    rental = models.ForeignKey(
        Rental,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Заказ'
    )
    
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Оценка (1-5)'
    )
    
    comment = models.TextField(
        verbose_name='Комментарий'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
        unique_together = ['user', 'equipment', 'rental']
    
    def __str__(self):
        return f"Отзыв от {self.user.username} - {self.rating}★"
    

class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
    
    def __str__(self):
        return f"Корзина {self.user.username}"
    
    @property
    def total_items(self):
        return self.items.count()
    
    @property
    def total_price(self):
        total = sum(item.subtotal for item in self.items.all())
        return total
    
    def clear(self):
        self.items.all().delete()


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Корзина'
    )
    
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name='Инвентарь'
    )
    
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name='Количество'
    )
    
    start_date = models.DateField(
        verbose_name='Дата начала аренды'
    )
    
    end_date = models.DateField(
        verbose_name='Дата окончания аренды'
    )
    
    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Скидка (руб.)'
    )
    
    added_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )
    
    class Meta:
        verbose_name = 'Позиция корзины'
        verbose_name_plural = 'Позиции корзины'
        unique_together = ['cart', 'equipment', 'start_date', 'end_date']
    
    def __str__(self):
        return f"{self.equipment.name} x{self.quantity}"
    
    @property
    def days(self):
        return (self.end_date - self.start_date).days + 1
    
    @property
    def subtotal(self):
        base_price = self.equipment.price_per_day * self.quantity * self.days
        return base_price - self.discount