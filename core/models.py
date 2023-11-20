from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
import random

class DeliveryAgent(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=15, blank=True, null=True)
    is_blocked = models.BooleanField(default=False)

    def generate_password(self):
        self.password = get_random_string(10)
        self.save()


class User(AbstractUser):
    pass

class Customer(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)
    is_blocked = models.BooleanField(default=False)
    is_soft_deleted = models.BooleanField(default=False)

    def __str__(self):
            return f'{self.name}'

    def softly_delete(self):
        self.is_soft_deleted = True
        self.save()

    @property
    def total_orders(self):
        total_orders = 0
        orders = Order.objects.filter(customer__id=self.id)
        if orders.__len__() > 0:
            total_orders = orders.__len__()
        return total_orders

    @property
    def total_amount(self):
        total_amount = 0
        orders = Order.objects.filter(customer__id=self.id)
        if orders.__len__() > 0:
            for order in orders:
                food_products = order.food_products
                total_amount = sum(list(map( lambda x: float(x[0]), food_products.values_list('price'))))
        return total_amount

class FoodProduct(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()

    def __str__(self):
        return f'{self.name}'
    
class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'PENDING'),
        ('ASSIGNED', 'ASSIGNED'),
        ('DELIVERED', 'DELIVERED'),
        ('CANCELLED', 'CANCELLED'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    customer_email = models.EmailField()
    customer_name = models.CharField(max_length=50, blank=True, null=True)
    food_products = models.ManyToManyField(FoodProduct)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    delivery_agent = models.ForeignKey(DeliveryAgent, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    otp = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'Order - {self.id}'
    
    def generate_otp(self):
        self.otp = random.randint(100000, 999999)
        self.save()

    def cancel_order(self):
        self.status = 'CANCELLED'
        self.save()

