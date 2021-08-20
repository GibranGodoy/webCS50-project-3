from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=64)
    def __str__(self):
        return f"{self.name}"

class regular(models.Model):
    name=models.CharField(max_length=64)
    small=models.DecimalField(max_digits=4, decimal_places=2)
    large=models.DecimalField(max_digits=4, decimal_places=2)
    def __str__(self):
        return f"Regular {self.name}: {self.small} - {self.large}"

class sicilian(models.Model):
    name=models.CharField(max_length=64)
    small=models.DecimalField(max_digits=4, decimal_places=2)
    large=models.DecimalField(max_digits=4, decimal_places=2)
    def __str__(self):
        return f"Sicilian {self.name}: {self.small} - {self.large}"

class toppings(models.Model):
    name=models.CharField(max_length=64)
    def __str__(self):
        return f"{self.name}"

class subs(models.Model):
    name=models.CharField(max_length=64)
    small=models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    large=models.DecimalField(max_digits=4, decimal_places=2)
    def __str__(self):
        return f"Sub {self.name}: {self.small} - {self.large}"

class pasta(models.Model):
    name=models.CharField(max_length=64)
    price=models.DecimalField(max_digits=4, decimal_places=2)
    def __str__(self):
        return f"Pasta {self.name}: {self.price}"

class salad(models.Model):
    name=models.CharField(max_length=64)
    price=models.DecimalField(max_digits=4, decimal_places=2)
    def __str__(self):
        return f"Salad {self.name}: {self.price}"

class dinner_platter(models.Model):
    name=models.CharField(max_length=64)
    small=models.DecimalField(max_digits=4, decimal_places=2)
    large=models.DecimalField(max_digits=4, decimal_places=2)
    def __str__(self):
        return f"Dinner Platter {self.name}: {self.small} - {self.large}"

class User_order(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    order_number=models.IntegerField()
    topping=models.IntegerField(default=0)
    status=models.CharField(max_length=64, default="On course")
    def __str__(self):
        return f"{self.user}: {self.order_number} [{self.status}] Mount of toppings: {self.topping}"

class order_cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    number=models.IntegerField()
    category=models.CharField(max_length=64, null=True)
    name=models.CharField(max_length=64)
    price=models.DecimalField(max_digits=4, decimal_places=2)
    def __str__(self):
        return f"{self.name} - ${self.price}"

class Order_counter(models.Model):
    counter=models.IntegerField()

    def __str__(self):
        return f"Order no: {self.counter}  "