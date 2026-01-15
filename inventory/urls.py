from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.catalog_view, name='catalog'),
    path('<slug:slug>/', views.equipment_detail_view, name='equipment_detail'),
    path('category/<slug:category_slug>/', views.category_view, name='category'),
]