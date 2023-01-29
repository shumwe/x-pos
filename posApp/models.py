from datetime import datetime
from unicodedata import category
from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from datetime import datetime

# Create your models here.

# class Employees(models.Model):
#     code = models.CharField(max_length=100,blank=True) 
#     firstname = models.TextField() 
#     middlename = models.TextField(blank=True,null= True) 
#     lastname = models.TextField() 
#     gender = models.TextField(blank=True,null= True) 
#     dob = models.DateField(blank=True,null= True) 
#     contact = models.TextField() 
#     address = models.TextField() 
#     email = models.TextField() 
#     department_id = models.ForeignKey(Department, on_delete=models.CASCADE) 
#     position_id = models.ForeignKey(Position, on_delete=models.CASCADE) 
#     date_hired = models.DateField() 
#     salary = models.FloatField(default=0) 
#     status = models.IntegerField() 
#     date_added = models.DateTimeField(default=timezone.now) 
#     date_updated = models.DateTimeField(auto_now=True) 

    # def __str__(self):
    #     return self.firstname + ' ' +self.middlename + ' '+self.lastname + ' '

def avatar_path(instance, filename):
    return f"avatars/{instance.customer_id}/{filename}"

class TrustedCustomerProfile(models.Model):
    name = models.CharField(max_length=65)
    email = models.EmailField(null=True, blank=True)
    avatar = models.ImageField(upload_to=avatar_path, default="ava.jpg", blank=True)
    slug = models.SlugField(unique=True, blank=True, verbose_name="Customer Id")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = '-'.join((slugify(self.name), slugify(datetime.now())))
        return super(TrustedCustomerProfile, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

class Category(models.Model):
    name = models.TextField()
    description = models.TextField()
    status = models.IntegerField(default=1) 
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = verbose_name

def product_image_path(instance, filename):
    return f"product/{instance.code}/{filename}"

class Products(models.Model):
    code = models.CharField(max_length=100)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.TextField()
    description = models.TextField()
    buying_price = models.FloatField(default=0)
    price = models.FloatField(default=0)
    status = models.IntegerField(default=1)
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True)
    bought_count = models.IntegerField(default=0)
    product_count = models.IntegerField(default=10)
    measurement_units = models.CharField(max_length=55, default="units")
    minimum_stock = models.IntegerField(default=1, help_text="warning, low stock!!!")
    image = models.ImageField(default="default-image.jpg")

    def __str__(self):
        return self.code + " - " + self.name
    
    @property
    def is_low_stock(self):
        if self.minimum_stock >= self.product_count:
            return True
        else:
            return False
            
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = verbose_name

class Sales(models.Model):
    code = models.CharField(max_length=100)
    sub_total = models.FloatField(default=0)
    grand_total = models.FloatField(default=0)
    tax_amount = models.FloatField(default=0)
    tax = models.FloatField(default=0)
    tendered_amount = models.FloatField(default=0)
    amount_change = models.FloatField(default=0)
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey(TrustedCustomerProfile, on_delete=models.CASCADE, related_name="customer", null=True, blank=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Sales"
        verbose_name_plural = verbose_name

class salesItems(models.Model):
    sale_id = models.ForeignKey(Sales, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products,on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    qty = models.FloatField(default=0)
    total = models.FloatField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Sales Items"
        verbose_name_plural = verbose_name


class ProductReturns(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="product")
    return_quantity = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Product Returns"
        verbose_name_plural = verbose_name

class Notify(models.Model):
    title = models.CharField(max_length=155)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="product_notify")
    resolved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Low Stock Notifications"
        verbose_name_plural = verbose_name