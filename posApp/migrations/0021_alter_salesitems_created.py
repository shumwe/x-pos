# Generated by Django 3.2.5 on 2023-01-24 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posApp', '0020_salesitems_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesitems',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
