# Generated by Django 3.2.5 on 2023-01-19 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posApp', '0011_auto_20230119_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='notify',
            name='resolved',
            field=models.BooleanField(default=False),
        ),
    ]
