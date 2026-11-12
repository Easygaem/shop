from django.contrib import admin
from .models import Product, Manufacturer

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'manufacturer', 'in_stock', 'created_at')
    list_filter = ('in_stock', 'manufacturer')
    search_fields = ('title',)