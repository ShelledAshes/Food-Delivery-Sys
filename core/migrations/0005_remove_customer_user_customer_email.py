# Generated by Django 4.2.6 on 2023-11-19 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_customer_total_amount_received_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='user',
        ),
        migrations.AddField(
            model_name='customer',
            name='email',
            field=models.EmailField(default='example@email.com', max_length=254, unique=True),
            preserve_default=False,
        ),
    ]
