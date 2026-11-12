from django.shortcuts import render, get_object_or_404
from .models import Product
from django.utils import timezone
from datetime import timedelta

def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'product_list.html', {'products': products, 'title': 'Каталог товаров'})

def new_products(request):
    one_week_ago = timezone.now() - timedelta(days=7)
    products = Product.objects.filter(created_at__gte=one_week_ago).order_by('-created_at')
    return render(request, 'product_list.html', {'products': products, 'title': 'Новинки (менее недели назад)'})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product, 'title': product.title})