from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Category, Equipment


def catalog_view(request):
    equipment_list = Equipment.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)
    
    search_query = request.GET.get('search', '')
    if search_query:
        equipment_list = equipment_list.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(brand__icontains=search_query)
        )
    
    category_slug = request.GET.get('category', '')
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        equipment_list = equipment_list.filter(category=selected_category)
    
    availability = request.GET.get('availability', '')
    if availability == 'available':
        equipment_list = equipment_list.filter(quantity_available__gt=0)
    elif availability == 'unavailable':
        equipment_list = equipment_list.filter(quantity_available=0)
    
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    if min_price:
        equipment_list = equipment_list.filter(price_per_day__gte=min_price)
    if max_price:
        equipment_list = equipment_list.filter(price_per_day__lte=max_price)
    
    condition = request.GET.get('condition', '')
    if condition:
        equipment_list = equipment_list.filter(condition=condition)
    
    sort_by = request.GET.get('sort', '-created_at')
    valid_sorts = ['price_per_day', '-price_per_day', 'name', '-name', '-created_at', 'created_at']
    if sort_by in valid_sorts:
        equipment_list = equipment_list.order_by(sort_by)
    
    context = {
        'equipment_list': equipment_list,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query,
        'sort_by': sort_by,
        'conditions': Equipment.Condition.choices,
    }
    
    return render(request, 'inventory/catalog.html', context)


def equipment_detail_view(request, slug):
    equipment = get_object_or_404(Equipment, slug=slug, is_active=True)

    similar_equipment = Equipment.objects.filter(
        category=equipment.category,
        is_active=True
    ).exclude(id=equipment.id)[:4]
    
    context = {
        'equipment': equipment,
        'similar_equipment': similar_equipment,
    }
    
    return render(request, 'inventory/equipment_detail.html', context)


def category_view(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug, is_active=True)
    equipment_list = Equipment.objects.filter(
        category=category,
        is_active=True
    ).order_by('-created_at')
    
    context = {
        'category': category,
        'equipment_list': equipment_list,
    }
    
    return render(request, 'inventory/category.html', context)