# Generated by Django 3.2.5 on 2023-01-17 22:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posApp', '0006_products_measurement_units'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='product', to='posApp.products'),
        ),
    ]
