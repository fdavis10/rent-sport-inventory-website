from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta
from .decorators import admin_required, staff_required
from accounts.models import User
from inventory.models import Category, Equipment
from rentals.models import Rental, RentalItem

@staff_required
def dashboard_view(request):
    

    stats = {
        'total_users': User.objects.filter(role='CLIENT').count(),
        'active_rentals': Rental.objects.filter(status='ACTIVE').count(),
        'available_equipment': Equipment.objects.filter(
            is_active=True, 
            quantity_available__gt=0
        ).count(),
    }
    

    month_ago = timezone.now() - timedelta(days=30)
    monthly_revenue = Rental.objects.filter(
        created_at__gte=month_ago,
        status__in=['ACTIVE', 'COMPLETED']
    ).aggregate(total=Sum('total_price'))['total'] or 0
    stats['monthly_revenue'] = monthly_revenue
    

    stats['pending_count'] = Rental.objects.filter(status='PENDING').count()
    stats['confirmed_count'] = Rental.objects.filter(status='CONFIRMED').count()
    stats['active_count'] = Rental.objects.filter(status='ACTIVE').count()
    stats['completed_count'] = Rental.objects.filter(status='COMPLETED').count()
    stats['cancelled_count'] = Rental.objects.filter(status='CANCELLED').count()
    stats['total_rentals'] = Rental.objects.count()
    

    recent_rentals = Rental.objects.select_related('user').order_by('-created_at')[:10]
    

    popular_equipment = RentalItem.objects.values(
        'equipment__name', 
        'equipment__price_per_day'
    ).annotate(
        rental_count=Count('id')
    ).order_by('-rental_count')[:5]
    
    context = {
        'stats': stats,
        'recent_rentals': recent_rentals,
        'popular_equipment': popular_equipment,
    }
    
    return render(request, 'custom_admin/dashboard.html', context)

@staff_required
def rentals_list_view(request):
    
    rentals = Rental.objects.select_related('user').order_by('-created_at')
    

    status_filter = request.GET.get('status')
    if status_filter:
        rentals = rentals.filter(status=status_filter)
    
    search_query = request.GET.get('search')
    if search_query:
        rentals = rentals.filter(
            Q(id__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(user__email__icontains=search_query)
        )
    
    context = {
        'rentals': rentals,
        'status_choices': Rental.Status.choices,
        'status_filter': status_filter,
        'search_query': search_query,
    }
    
    return render(request, 'custom_admin/rentals/list.html', context)


@staff_required
def rental_detail_view(request, pk):
    
    rental = get_object_or_404(Rental.objects.select_related('user'), id=pk)
    rental_items = rental.items.select_related('equipment')
    
    context = {
        'rental': rental,
        'rental_items': rental_items,
    }
    
    return render(request, 'custom_admin/rentals/detail.html', context)


@staff_required
def rental_update_status_view(request, pk):
    
    rental = get_object_or_404(Rental, id=pk)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        
        if new_status in dict(Rental.Status.choices):
            old_status = rental.status
            rental.status = new_status
            
            if new_status == 'CONFIRMED' and old_status == 'PENDING':
                rental.confirmed_by = request.user
                rental.confirmed_at = timezone.now()
            
            rental.save()
            
            messages.success(
                request, 
                f'Статус заказа №{rental.id} изменён: {rental.get_status_display()}'
            )
        else:
            messages.error(request, 'Неверный статус')
    
    return redirect('custom_admin:rental_detail', pk=pk)


@admin_required
def categories_list_view(request):
    
    categories = Category.objects.annotate(
        equipment_count=Count('equipment')
    ).order_by('name')
    
    context = {
        'categories': categories,
    }
    
    return render(request, 'custom_admin/categories/list.html', context)


@admin_required
def category_create_view(request):
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        is_active = request.POST.get('is_active') == 'on'
        image = request.FILES.get('image')
        
        if name:
            from django.utils.text import slugify
            slug = slugify(name)
            
            if Category.objects.filter(slug=slug).exists():
                messages.error(request, 'Категория с таким названием уже существует')
            else:
                category = Category.objects.create(
                    name=name,
                    slug=slug,
                    description=description,
                    is_active=is_active,
                    image=image
                )
                messages.success(request, f'Категория "{category.name}" создана')
                return redirect('custom_admin:categories_list')
        else:
            messages.error(request, 'Укажите название категории')
    
    return render(request, 'custom_admin/categories/create.html')


@admin_required
def category_edit_view(request, pk):
    
    category = get_object_or_404(Category, id=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        is_active = request.POST.get('is_active') == 'on'
        image = request.FILES.get('image')
        
        if name:
            category.name = name
            category.description = description
            category.is_active = is_active
            
            if image:
                category.image = image
            
            category.save()
            
            messages.success(request, f'Категория "{category.name}" обновлена')
            return redirect('custom_admin:categories_list')
        else:
            messages.error(request, 'Укажите название категории')
    
    context = {
        'category': category,
    }
    
    return render(request, 'custom_admin/categories/edit.html', context)


@admin_required
def category_delete_view(request, pk):
    
    category = get_object_or_404(Category, id=pk)
    
    if category.equipment.exists():
        messages.error(
            request, 
            f'Невозможно удалить категорию "{category.name}" - к ней привязаны товары'
        )
    else:
        name = category.name
        category.delete()
        messages.success(request, f'Категория "{name}" удалена')
    
    return redirect('custom_admin:categories_list')

@admin_required
def equipment_list_view(request):

    
    equipment_list = Equipment.objects.select_related('category').order_by('-created_at')
    

    category_filter = request.GET.get('category')
    if category_filter:
        equipment_list = equipment_list.filter(category__slug=category_filter)
    
    search_query = request.GET.get('search')
    if search_query:
        equipment_list = equipment_list.filter(
            Q(name__icontains=search_query) |
            Q(brand__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'equipment_list': equipment_list,
        'categories': categories,
        'category_filter': category_filter,
        'search_query': search_query,
    }
    
    return render(request, 'custom_admin/equipment/list.html', context)


@admin_required
def equipment_create_view(request):

    
    if request.method == 'POST':
        category_id = request.POST.get('category')
        name = request.POST.get('name')
        description = request.POST.get('description')
        brand = request.POST.get('brand', '')
        model = request.POST.get('model', '')
        size = request.POST.get('size')
        condition = request.POST.get('condition')
        price_per_day = request.POST.get('price_per_day')
        quantity_total = request.POST.get('quantity_total')
        quantity_available = request.POST.get('quantity_available')
        is_active = request.POST.get('is_active') == 'on'
        image = request.FILES.get('image')
        
        if all([category_id, name, description, size, price_per_day, quantity_total, quantity_available, image]):
            from django.utils.text import slugify
            slug = slugify(f"{name}-{size}")
            
            if Equipment.objects.filter(slug=slug).exists():
                messages.error(request, 'Инвентарь с таким названием и размером уже существует')
            else:
                category = Category.objects.get(id=category_id)
                
                equipment = Equipment.objects.create(
                    category=category,
                    name=name,
                    slug=slug,
                    description=description,
                    brand=brand,
                    model=model,
                    size=size,
                    condition=condition,
                    price_per_day=price_per_day,
                    quantity_total=quantity_total,
                    quantity_available=quantity_available,
                    is_active=is_active,
                    image=image
                )
                
                messages.success(request, f'Инвентарь "{equipment.name}" создан')
                return redirect('custom_admin:equipment_list')
        else:
            messages.error(request, 'Заполните все обязательные поля')
    
    categories = Category.objects.filter(is_active=True)
    conditions = Equipment.Condition.choices
    
    context = {
        'categories': categories,
        'conditions': conditions,
    }
    
    return render(request, 'custom_admin/equipment/create.html', context)


@admin_required
def equipment_edit_view(request, pk):
    
    equipment = get_object_or_404(Equipment, id=pk)
    
    if request.method == 'POST':
        category_id = request.POST.get('category')
        name = request.POST.get('name')
        description = request.POST.get('description')
        brand = request.POST.get('brand', '')
        model = request.POST.get('model', '')
        size = request.POST.get('size')
        condition = request.POST.get('condition')
        price_per_day = request.POST.get('price_per_day')
        quantity_total = request.POST.get('quantity_total')
        quantity_available = request.POST.get('quantity_available')
        is_active = request.POST.get('is_active') == 'on'
        image = request.FILES.get('image')
        
        if all([category_id, name, description, size, price_per_day, quantity_total, quantity_available]):
            equipment.category = Category.objects.get(id=category_id)
            equipment.name = name
            equipment.description = description
            equipment.brand = brand
            equipment.model = model
            equipment.size = size
            equipment.condition = condition
            equipment.price_per_day = price_per_day
            equipment.quantity_total = quantity_total
            equipment.quantity_available = quantity_available
            equipment.is_active = is_active
            
            if image:
                equipment.image = image
            
            equipment.save()
            
            messages.success(request, f'Инвентарь "{equipment.name}" обновлён')
            return redirect('custom_admin:equipment_list')
        else:
            messages.error(request, 'Заполните все обязательные поля')
    
    categories = Category.objects.filter(is_active=True)
    conditions = Equipment.Condition.choices
    
    context = {
        'equipment': equipment,
        'categories': categories,
        'conditions': conditions,
    }
    
    return render(request, 'custom_admin/equipment/edit.html', context)


@admin_required
def equipment_delete_view(request, pk):
    """Удаление инвентаря (только ADMIN)"""
    
    equipment = get_object_or_404(Equipment, id=pk)
    
    if equipment.rental_items.exists():
        messages.error(
            request, 
            f'Невозможно удалить "{equipment.name}" - есть связанные заказы'
        )
    else:
        name = equipment.name
        equipment.delete()
        messages.success(request, f'Инвентарь "{name}" удалён')
    
    return redirect('custom_admin:equipment_list')


@admin_required
def users_list_view(request):
    
    users = User.objects.order_by('-created_at')
    
    role_filter = request.GET.get('role')
    if role_filter:
        users = users.filter(role=role_filter)
    
    search_query = request.GET.get('search')
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    context = {
        'users': users,
        'role_choices': User.Role.choices,
        'role_filter': role_filter,
        'search_query': search_query,
    }
    
    return render(request, 'custom_admin/users/list.html', context)


@admin_required
def user_edit_view(request, pk):
    
    user = get_object_or_404(User, id=pk)
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        role = request.POST.get('role')
        is_active = request.POST.get('is_active') == 'on'
        
        if all([first_name, last_name, email, role]):
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.role = role
            user.is_active = is_active
            user.save()
            
            messages.success(request, f'Пользователь {user.get_full_name()} обновлён')
            return redirect('custom_admin:users_list')
        else:
            messages.error(request, 'Заполните все обязательные поля')
    
    context = {
        'edited_user': user,
        'role_choices': User.Role.choices,
    }
    
    return render(request, 'custom_admin/users/edit.html', context)


@admin_required
def user_delete_view(request, pk):
    
    user = get_object_or_404(User, id=pk)
    
    if user == request.user:
        messages.error(request, 'Нельзя удалить свой собственный аккаунт')
        return redirect('custom_admin:users_list')
    
    if user.rentals.exists():
        messages.error(
            request, 
            f'Невозможно удалить пользователя {user.get_full_name()} - есть связанные заказы'
        )
    else:
        name = user.get_full_name()
        user.delete()
        messages.success(request, f'Пользователь {name} удалён')
    
    return redirect('custom_admin:users_list')