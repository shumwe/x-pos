# Generated by Django 3.2.5 on 2023-01-24 09:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posApp', '0015_alter_trusecustomerprofile_customer_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TruseCustomerProfile',
            new_name='TrustedCustomerProfile',
        ),
    ]
