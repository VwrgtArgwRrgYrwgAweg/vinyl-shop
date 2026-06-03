from django.contrib import admin
from .models import Product, Order, OrderItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('artist', 'title', 'year', 'price', 'stock', 'genre', 'created_at')
    list_filter = ('genre', 'year')
    search_fields = ('artist', 'title')
    fields = ('artist', 'title', 'year', 'price', 'stock', 'genre', 'image', 'image_url', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'phone', 'total', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('full_name', 'email', 'phone')
    readonly_fields = ('created_at',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')