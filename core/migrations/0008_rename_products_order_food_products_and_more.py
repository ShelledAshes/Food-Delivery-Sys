# Generated by Django 4.2.6 on 2023-11-19 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_order_otp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='products',
            new_name='food_products',
        ),
        migrations.RemoveField(
            model_name='order',
            name='is_soft_deleted',
        ),
    ]