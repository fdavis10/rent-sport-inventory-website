from django.shortcuts import render
from inventory.models import Category, Equipment


def index_view(request):
    categories = Category.objects.filter(is_active=True)
    popular_equipment = Equipment.objects.filter(
        is_active=True,
        quantity_available__gt=0
    ).order_by('-created_at')[:8]
    
    context = {
        'categories': categories,
        'popular_equipment': popular_equipment,
    }
    return render(request, 'core/index.html', context)


def about_view(request):
    return render(request, 'core/about.html')