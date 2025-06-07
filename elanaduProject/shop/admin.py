from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'available', 'slug']
    list_filter = ['category', 'available']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
