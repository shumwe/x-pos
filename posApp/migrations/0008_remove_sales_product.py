# Generated by Django 3.2.5 on 2023-01-17 22:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posApp', '0007_sales_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sales',
            name='product',
        ),
    ]
