from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'format', 'package')
    list_filter = ('available', 'category', 'created')
    search_fields = ('name', 'format', 'package')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created', 'updated')

