"""
Логика управления корзиной и расчёта стоимости аренды оборудования
"""
from decimal import Decimal
from datetime import date, timedelta
from .models import Cart, CartItem


def get_or_create_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


def add_to_cart(user, equipment, quantity, start_date, end_date):
    cart = get_or_create_cart(user)
    
    if equipment.quantity_available < quantity:
        return False, "Недостаточно товара в наличии"
    
    if start_date < date.today():
        return False, "Дата начала не может быть в прошлом"
    
    if end_date <= start_date:
        return False, "Дата окончания должна быть позже даты начала"
    
    # Рассчитываем скидку
    cost_info = calculate_rental_cost(equipment, quantity, start_date, end_date)
    discount = cost_info['discount']
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        equipment=equipment,
        start_date=start_date,
        end_date=end_date,
        defaults={'quantity': quantity, 'discount': discount}
    )
    
    if not created:
        new_quantity = cart_item.quantity + quantity
        if new_quantity > equipment.quantity_available:
            return False, "Превышено доступное количество"
        cart_item.quantity = new_quantity
        # Пересчитываем скидку с новым количеством
        cost_info = calculate_rental_cost(equipment, new_quantity, start_date, end_date)
        cart_item.discount = cost_info['discount']
        cart_item.save()
    
    return True, "Товар добавлен в корзину"


def remove_from_cart(user, cart_item_id):
    try:
        cart = get_or_create_cart(user)
        cart_item = CartItem.objects.get(id=cart_item_id, cart=cart)
        cart_item.delete()
        return True, "Товар удалён из корзины"
    except CartItem.DoesNotExist:
        return False, "Товар не найден в корзине"


def update_cart_item(user, cart_item_id, quantity):
    try:
        cart = get_or_create_cart(user)
        cart_item = CartItem.objects.get(id=cart_item_id, cart=cart)
        
        if quantity <= 0:
            cart_item.delete()
            return True, "Товар удалён"
        
        if quantity > cart_item.equipment.quantity_available:
            return False, "Превышено доступное количество"
        
        cart_item.quantity = quantity
        # Пересчитываем скидку с новым количеством
        cost_info = calculate_rental_cost(cart_item.equipment, quantity, cart_item.start_date, cart_item.end_date)
        cart_item.discount = cost_info['discount']
        cart_item.save()
        return True, "Количество обновлено"
    except CartItem.DoesNotExist:
        return False, "Товар не найден"


def calculate_rental_cost(equipment, quantity, start_date, end_date):
    days = (end_date - start_date).days + 1
    total = equipment.price_per_day * quantity * days
    
    discount = Decimal('0')
    
    if days >= 7:
        discount = total * Decimal('0.10')
    
    elif days >= 3:
        discount = total * Decimal('0.05')
    
    final_price = total - discount
    
    return {
        'base_price': equipment.price_per_day,
        'quantity': quantity,
        'days': days,
        'subtotal': total,
        'discount': discount,
        'discount_percent': (discount / total * 100) if total > 0 else 0,
        'total': final_price,
    }