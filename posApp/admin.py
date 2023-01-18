from django.contrib import admin

from posApp.models import Category, ProductReturns, Products, Sales, salesItems

# Register your models here.
admin.site.register(Category)
admin.site.register(Products)
admin.site.register(Sales)
admin.site.register(ProductReturns)
admin.site.register(salesItems)
# admin.site.register(Employees)