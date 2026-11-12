from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('new/', views.new_products, name='new_products'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
]