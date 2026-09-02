from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import Category, Product, ProductImage


class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ["name", "parent", "is_active"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ["name", "category", "price", "stock_quantity", "is_active", "updated_at"]
    list_filter = ["is_active", "category"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]
