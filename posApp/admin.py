from django.contrib import admin

from posApp.models import Category, ProductReturns, Products, Sales, salesItems, Notify

# Register your models here.
# admin.site.register(Employees)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "status", "date_added"]

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ["code", "category_id", "name", "price", "status", "product_count", "measurement_units"]

@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    list_display = ["code", "grand_total", "tendered_amount", "date_added"]

@admin.register(ProductReturns)
class ProductReturnsAdmin(admin.ModelAdmin):
    list_display = ["product", "return_quantity", "created"]

@admin.register(salesItems)
class salesItemsAdmin(admin.ModelAdmin):
    list_display = ["sale_id", "product_id", "price", "qty", "total"]

@admin.register(Notify)
class NotifyAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "product", "resolved", "created"]