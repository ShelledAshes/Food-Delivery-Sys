# Generated by Django 4.2.6 on 2023-11-19 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_deliveryagent_otp_order_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='otp',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]