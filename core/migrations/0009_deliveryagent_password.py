# Generated by Django 4.2.6 on 2023-11-19 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_rename_products_order_food_products_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryagent',
            name='password',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]