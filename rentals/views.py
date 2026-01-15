from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from datetime import date, timedelta
from .models import Rental, CartItem
from .utils import get_or_create_cart, add_to_cart, remove_from_cart, update_cart_item, calculate_rental_cost
from inventory.models import Equipment


@login_required
def cart_view(request):
    cart = get_or_create_cart(request.user)
    cart_items = cart.items.all().select_related('equipment')
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    
    return render(request, 'rentals/cart.html', context)


@login_required
def add_to_cart_view(request, equipment_id):
    equipment = get_object_or_404(Equipment, id=equipment_id, is_active=True)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        
        try:
            from datetime import datetime
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            messages.error(request, 'Некорректные даты')
            return redirect('inventory:equipment_detail', slug=equipment.slug)
        
        success, message = add_to_cart(request.user, equipment, quantity, start_date, end_date)
        
        if success:
            messages.success(request, message)
            return redirect('rentals:cart')
        else:
            messages.error(request, message)
            return redirect('inventory:equipment_detail', slug=equipment.slug)
    
    default_start = date.today() + timedelta(days=1)
    default_end = default_start + timedelta(days=2)
    
    context = {
        'equipment': equipment,
        'default_start': default_start,
        'default_end': default_end,
    }
    
    return render(request, 'rentals/add_to_cart.html', context)


@login_required
def remove_from_cart_view(request, cart_item_id):
    success, message = remove_from_cart(request.user, cart_item_id)
    
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)
    
    return redirect('rentals:cart')


@login_required
def update_cart_item_view(request, cart_item_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        success, message = update_cart_item(request.user, cart_item_id, quantity)
        
        cart = get_or_create_cart(request.user)
        
        return JsonResponse({
            'success': success,
            'message': message,
            'cart_total': float(cart.total_price),
            'cart_items_count': cart.total_items,
        })
    
    return JsonResponse({'success': False, 'message': 'Метод не поддерживается'})


@login_required
def checkout_view(request):
    cart = get_or_create_cart(request.user)
    
    if not cart.items.exists():
        messages.warning(request, 'Корзина пуста')
        return redirect('inventory:catalog')
    
    if request.method == 'POST':
        comment = request.POST.get('comment', '')
        
        first_item = cart.items.first()
        
        rental = Rental.objects.create(
            user=request.user,
            start_date=first_item.start_date,
            end_date=first_item.end_date,
            total_price=cart.total_price,
            comment=comment,
            status=Rental.Status.PENDING
        )
        
        from .models import RentalItem
        
        for cart_item in cart.items.all():
            RentalItem.objects.create(
                rental=rental,
                equipment=cart_item.equipment,
                quantity=cart_item.quantity,
                price_per_day=cart_item.equipment.price_per_day,
                days=cart_item.days,
            )
            
            cart_item.equipment.quantity_available -= cart_item.quantity
            cart_item.equipment.save()
        
        cart.clear()
        
        messages.success(request, f'Заказ №{rental.id} успешно создан! Ожидайте подтверждения.')
        return redirect('rentals:rental_detail', rental_id=rental.id)
    
    context = {
        'cart': cart,
        'cart_items': cart.items.all(),
    }
    
    return render(request, 'rentals/checkout.html', context)


@login_required
def my_rentals_view(request):
    rentals = Rental.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'rentals': rentals,
    }
    
    return render(request, 'rentals/my_rentals.html', context)


@login_required
def rental_detail_view(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id, user=request.user)
    
    context = {
        'rental': rental,
    }
    
    return render(request, 'rentals/rental_detail.html', context)


@login_required
def calculate_cost_ajax(request):
    if request.method == 'POST':
        try:
            equipment_id = int(request.POST.get('equipment_id'))
            quantity = int(request.POST.get('quantity', 1))
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            
            from datetime import datetime
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            equipment = Equipment.objects.get(id=equipment_id)
            
            cost_data = calculate_rental_cost(equipment, quantity, start_date, end_date)
            
            return JsonResponse({
                'success': True,
                'data': {
                    'base_price': float(cost_data['base_price']),
                    'quantity': cost_data['quantity'],
                    'days': cost_data['days'],
                    'subtotal': float(cost_data['subtotal']),
                    'discount': float(cost_data['discount']),
                    'discount_percent': float(cost_data['discount_percent']),
                    'total': float(cost_data['total']),
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Метод не поддерживается'})