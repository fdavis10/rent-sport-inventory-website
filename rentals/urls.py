from django.urls import path
from . import views

app_name = 'rentals'

urlpatterns = [
    # сart
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:equipment_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart_view, name='remove_from_cart'),
    path('update-cart-item/<int:cart_item_id>/', views.update_cart_item_view, name='update_cart_item'),
    
    # checkout
    path('checkout/', views.checkout_view, name='checkout'),
    
    # my rentals
    path('my-rentals/', views.my_rentals_view, name='my_rentals'),
    path('rental/<int:rental_id>/', views.rental_detail_view, name='rental_detail'),
    
    # AJAX
    path('calculate-cost/', views.calculate_cost_ajax, name='calculate_cost'),
]