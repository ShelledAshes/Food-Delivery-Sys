# Generated by Django 4.2.6 on 2023-11-20 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_customer_name_order_customer_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='is_soft_deleted',
            field=models.BooleanField(default=False),
        ),
    ]