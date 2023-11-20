# Generated by Django 4.2.6 on 2023-11-19 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_blocked_deliveryagent_is_blocked_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='total_orders',
        ),
        migrations.RemoveField(
            model_name='foodproduct',
            name='image',
        ),
        migrations.AddField(
            model_name='customer',
            name='is_blocked',
            field=models.BooleanField(default=False),
        ),
    ]