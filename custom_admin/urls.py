from django.urls import path
from . import views

app_name = 'custom_admin'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),

    path('categories/', views.categories_list_view, name='categories_list'),
    path('categories/create/', views.category_create_view, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_edit_view, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete_view, name='category_delete'),

    path('equipment/', views.equipment_list_view, name='equipment_list'),
    path('equipment/create/', views.equipment_create_view, name='equipment_create'),
    path('equipment/<int:pk>/edit/', views.equipment_edit_view, name='equipment_edit'),
    path('equipment/<int:pk>/delete/', views.equipment_delete_view, name='equipment_delete'),
    
    path('users/', views.users_list_view, name='users_list'),
    path('users/<int:pk>/edit/', views.user_edit_view, name='user_edit'),
    path('users/<int:pk>/delete/', views.user_delete_view, name='user_delete'),
    
    path('rentals/', views.rentals_list_view, name='rentals_list'),
    path('rentals/<int:pk>/', views.rental_detail_view, name='rental_detail'),
    path('rentals/<int:pk>/update-status/', views.rental_update_status_view, name='rental_update_status'),
]