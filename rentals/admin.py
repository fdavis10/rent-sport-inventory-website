from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Rental, RentalItem, Review


class RentalItemInline(TabularInline):
    model = RentalItem
    extra = 0
    readonly_fields = ['subtotal']
    fields = ['equipment', 'quantity', 'price_per_day', 'days', 'subtotal']


@admin.register(Rental)
class RentalAdmin(ModelAdmin):
    list_display = [
        'id', 'user', 'status', 'start_date', 'end_date',
        'total_price', 'created_at'
    ]
    list_filter = ['status', 'created_at', 'start_date']
    search_fields = ['user__username', 'user__email', 'comment']
    readonly_fields = ['created_at', 'updated_at', 'duration_days']
    inlines = [RentalItemInline]
    
    fieldsets = (
        ('Информация о заказе', {
            'fields': ('user', 'status', 'total_price')
        }),
        ('Даты аренды', {
            'fields': ('start_date', 'end_date', 'duration_days')
        }),
        ('Дополнительно', {
            'fields': ('comment',)
        }),
        ('Подтверждение', {
            'fields': ('confirmed_by', 'confirmed_at')
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj and request.user.is_manager:
            return self.readonly_fields + ['total_price']
        return self.readonly_fields


@admin.register(RentalItem)
class RentalItemAdmin(ModelAdmin):
    list_display = ['rental', 'equipment', 'quantity', 'price_per_day', 'days', 'subtotal']
    list_filter = ['rental__status', 'rental__created_at']
    search_fields = ['equipment__name', 'rental__user__username']
    readonly_fields = ['subtotal']


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ['user', 'equipment', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'equipment__name', 'comment']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Информация об отзыве', {
            'fields': ('user', 'equipment', 'rental')
        }),
        ('Оценка', {
            'fields': ('rating', 'comment')
        }),
        ('Дата', {
            'fields': ('created_at',)
        }),
    )


from .models import Cart, CartItem


class CartItemInline(TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['subtotal', 'days']
    fields = ['equipment', 'quantity', 'start_date', 'end_date', 'days', 'subtotal']


@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = ['user', 'total_items', 'total_price', 'created_at', 'updated_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at', 'total_items', 'total_price']
    inlines = [CartItemInline]
    
    fieldsets = (
        ('Информация', {
            'fields': ('user', 'total_items', 'total_price')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(CartItem)
class CartItemAdmin(ModelAdmin):
    list_display = ['cart', 'equipment', 'quantity', 'start_date', 'end_date', 'days', 'subtotal']
    list_filter = ['start_date', 'end_date']
    search_fields = ['equipment__name', 'cart__user__username']
    readonly_fields = ['days', 'subtotal', 'added_at']