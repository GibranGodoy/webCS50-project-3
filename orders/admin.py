from django.contrib import admin
from .models import Category, regular, sicilian, toppings, subs, pasta, salad, dinner_platter, User_order, order_cart, Order_counter

# Register your models here.
admin.site.register(Category)
admin.site.register(regular)
admin.site.register(sicilian)
admin.site.register(toppings)
admin.site.register(subs)
admin.site.register(pasta)
admin.site.register(salad)
admin.site.register(dinner_platter)
admin.site.register(User_order)
admin.site.register(order_cart)
admin.site.register(Order_counter)