from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Category, Equipment


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Медиа', {
            'fields': ('image',)
        }),
        ('Настройки', {
            'fields': ('is_active',)
        }),
    )


@admin.register(Equipment)
class EquipmentAdmin(ModelAdmin):
    list_display = [
        'name', 'category', 'size', 'brand', 'condition',
        'price_per_day', 'quantity_available', 'is_active'
    ]
    list_filter = ['category', 'condition', 'is_active', 'created_at']
    search_fields = ['name', 'brand', 'model', 'description']
    prepopulated_fields = {'slug': ('name', 'size')}
    list_editable = ['price_per_day', 'quantity_available', 'is_active']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('category', 'name', 'slug', 'description')
        }),
        ('Характеристики', {
            'fields': ('brand', 'model', 'size', 'condition')
        }),
        ('Медиа', {
            'fields': ('image',)
        }),
        ('Цены и наличие', {
            'fields': ('price_per_day', 'quantity_total', 'quantity_available')
        }),
        ('Настройки', {
            'fields': ('is_active',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['slug', 'created_at', 'updated_at']
        return ['created_at', 'updated_at']