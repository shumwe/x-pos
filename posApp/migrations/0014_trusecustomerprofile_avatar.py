# Generated by Django 3.2.5 on 2023-01-24 09:07

from django.db import migrations, models
import posApp.models


class Migration(migrations.Migration):

    dependencies = [
        ('posApp', '0013_auto_20230124_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='trusecustomerprofile',
            name='avatar',
            field=models.ImageField(blank=True, default='ava.jpg', upload_to=posApp.models.avatar_path),
        ),
    ]
