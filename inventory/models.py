from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название'
    )
    
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='URL'
    )
    
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    
    image = models.ImageField(
        upload_to='categories/',
        null=True,
        blank=True,
        verbose_name='Изображение'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Equipment(models.Model):
    class Condition(models.TextChoices):
        EXCELLENT = 'EXCELLENT', 'Отличное'
        GOOD = 'GOOD', 'Хорошее'
        SATISFACTORY = 'SATISFACTORY', 'Удовлетворительное'
    
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='equipment',
        verbose_name='Категория'
    )
    
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='URL'
    )
    
    description = models.TextField(
        verbose_name='Описание'
    )
    
    image = models.ImageField(
        upload_to='equipment/',
        verbose_name='Изображение'
    )
    
    brand = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Бренд'
    )
    
    model = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Модель'
    )
    
    size = models.CharField(
        max_length=50,
        verbose_name='Размер'
    )
    
    condition = models.CharField(
        max_length=20,
        choices=Condition.choices,
        default=Condition.GOOD,
        verbose_name='Состояние'
    )
    
    price_per_day = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Цена за день (руб.)'
    )
    
    quantity_total = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name='Общее количество'
    )
    
    quantity_available = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(0)],
        verbose_name='Доступно для аренды'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    
    class Meta:
        verbose_name = 'Инвентарь'
        verbose_name_plural = 'Инвентарь'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.size})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.size}")
        super().save(*args, **kwargs)
    
    @property
    def is_available(self):
        return self.is_active and self.quantity_available > 0