from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.shortcuts import redirect
import datetime

# Create your models here.

WEEK_DAYS = (
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday'),
    (7, 'Sunday'),
)

class WeekDays(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class CoffeeType(models.Model):
    name = models.CharField(max_length=50)

    @staticmethod
    def get_all_coffee_type():
        return CoffeeType.objects.all()

    def __str__(self):
        return self.name

class TableType(models.Model):
    name = models.CharField(max_length=50)
    days_available = models.ManyToManyField(WeekDays, related_name="available_table_types")

class Table(models.Model):
    LOCATION_CHOICES=(
        ('out', 'Outside'),
        ('in', 'Inside'),
    )
    location = models.CharField(choices=LOCATION_CHOICES, max_length=5, default='out')
    capacity = models.IntegerField(default=0)
    day = models.CharField(null=True, blank=True, default=None, max_length=100)
    booking_time = models.CharField(null=True, blank=True, default=None, max_length=100)
    booked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tables_booked", blank=True, null=True)
    booked = models.BooleanField(default=False)

class Coffee(models.Model):
    STATUS_CHOICES=(
        ('in_s', 'In stock'),
        ('out_s', 'Out of stock'),
    )
    name = models.CharField(max_length=60)
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to='uploads/coffee/')
    age_limit = models.BooleanField(default=False)
    days_available = models.ManyToManyField(WeekDays, related_name="available_coffees")
    available_from = models.TimeField(auto_now_add=False, blank=True, null=True, default=None)
    available_to = models.TimeField(auto_now_add=False, blank=True, null=True, default=None)
    type = models.ForeignKey(CoffeeType, on_delete=models.CASCADE, default=1)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default='in_s')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_coffee_by_id(ids):
        return Coffee.objects.filter(id__in=ids)

    @staticmethod
    def get_all_coffee():
        return Coffee.objects.all()
  
    @staticmethod
    def get_all_coffee_by_category(category):
        return Coffee.objects.filter(category__name=category)

    @property
    def get_exerpt(self):
        try:
            return self.description[:50]
        except:
            return None

    @property
    def get_image_url(self):
        try:
            return self.image.url
        except:
            return ''

    @property
    def get_absolute_url(self):
        return f"{reverse('CoffeeDetailView', kwargs={'id':self.id})}"


class OrderItem(models.Model):
    item = models.ForeignKey(Coffee, on_delete=models.CASCADE, related_name="order_items")
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)
    date = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_order_item_by_id(ids):
        return OrderItem.objects.filter(product__id__in = ids)


class Order(models.Model):
    STATUS_CHOICES=(
        ('p', 'Order Placed'),
        ('c', 'Completed'),
    )
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    items = models.ManyToManyField(OrderItem, related_name="orders")
    price = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default='p')

    @staticmethod
    def get_orders_by_customer(customer_id):
        return OrderItem.objects.filter(customer=customer_id).order_by('-date')


