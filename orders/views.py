from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Sum
from .models import Category, regular, sicilian, toppings, subs, pasta, salad, dinner_platter, User_order, order_cart, Order_counter

# Create your views here.
counter = Order_counter.objects.first()
if counter==None:
    set_counter=Order_counter(counter=1)
    set_counter.save()

admin=User.objects.filter(is_superuser=True)
if admin.count()==0:
    admin=User.objects.create_user("admin", "admin@cs50.com", "admin")
    admin.is_superuser=True
    admin.is_staff=True
    admin.save()
    set_admin=User_order(user=admin, order_number=counter.counter)
    set_admin.save()

def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})
    order_number=User_order.objects.get(user=request.user, status="On course").order_number
    context={
        "user": request.user,
        "Checkout": order_cart.objects.filter(user=request.user, number=order_number),
        "Checkout_category": order_cart.objects.filter(user=request.user, number=order_number).values_list("category").distinct(),
        "Total": list(order_cart.objects.filter(user=request.user, number=order_number).aggregate(Sum("price")).values())[0],
        "Category": Category.objects.all(),
        "Order_number": order_number
    }
    return render(request, "orders/index.html", context)

def signin_view(request):
    if request.method=="POST":
        first_name=request.POST["first_name"]
        last_name=request.POST["last_name"]
        username=request.POST["username"]
        email=request.POST["email"]
        password=request.POST["password"]
        confirm_password=request.POST["confirm_password"]
        if not first_name.replace(" ",""):
            return render(request, "orders/signin.html", {"message": "Need the fist name"})
        elif not last_name.replace(" ",""):
            return render(request, "orders/signin.html", {"message": "Need the last name"})
        elif not username.replace(" ",""):
            return render(request, "orders/signin.html", {"message": "Need the username"})
        elif not email.replace(" ",""):
            return render(request, "orders/signin.html", {"message": "Need the email"})
        elif not password.replace(" ",""):
            return render(request, "orders/signin.html", {"message": "Need the password"})
        elif not confirm_password.replace(" ",""):
            return render(request, "orders/signin.html", {"message": "Please, confirm password"})
        elif not password==confirm_password:
            return render(request, "orders/signin.html", {"message": "Passwords don't match"})
        user=User.objects.create_user(username, email, password)
        user.first_name=first_name
        user.last_name=last_name
        user.save()
        counter=Order_counter.objects.first()
        order_number=User_order(user=user, order_number=counter.counter)
        order_number.save()
        counter.counter=counter.counter+1
        counter.save()
        return render(request, "orders/login.html", {"message": "Signed up"})
    return render(request, "orders/signin.html")

def login_view(request):
    if request.method=="GET":
        return render(request, "orders/login.html")
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "orders/login.html", {"message": "Invalid credentials."})

def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out."})

def menu(request, category):
    menu, columns=findTable(category)
    order_number=User_order.objects.get(user=request.user, status="On course").order_number
    context={
        "user": request.user,
        "Checkout": order_cart.objects.filter(user=request.user, number=order_number),
        "Checkout_category": order_cart.objects.filter(user=request.user, number=order_number).values_list("category").distinct(),
        "Total": list(order_cart.objects.filter(user=request.user,number=order_number).aggregate(Sum('price')).values())[0],
        "Category": Category.objects.all(),
        "Active_category": category,
        "Menu": menu,
        "Columns": columns,
        "Topping_price": 0.00,
        "Order_number": order_number
    }
    return render(request, "orders/menu.html", context)

def add(request, category, name, price):
    menu, columns=findTable(category)
    order_number=User_order.objects.get(user=request.user, status='On course').order_number
    topping=User_order.objects.get(user=request.user, status='On course')
    context = {
        "Checkout": order_cart.objects.filter(user=request.user,number=order_number),
        "Checkout_category": order_cart.objects.filter(user=request.user,number=order_number).values_list("category").distinct(),
        "Total": list(order_cart.objects.filter(user=request.user,number=order_number).aggregate(Sum("price")).values())[0],
        "user": request.user,
        "Category": Category.objects.all(),
        "Active_category": category,
        "Menu": menu,
        "Columns": columns,
        "Topping_price": 0.00,
        "Order_number": order_number
    }
    if (category == "Regular Pizza" or category == "Sicilian Pizza"):
        if name=="1 topping":
            topping.topping+=1
            topping.save()
        if name=="2 toppings":
            topping.topping+=2
            topping.save()
        if name=="3 toppings":
            topping.topping+=3    
            topping.save()
    if category == "Toppings" and topping.topping == 0:
        return render(request, "orders/menu.html", context) 
    if category == "Toppings" and topping.topping > 0:
        topping.topping-=1
        topping.save()

    add=order_cart(user=request.user, number=order_number, category=category, name=name, price=price) 
    add.save()      
    context2={
        "Checkout": order_cart.objects.filter(user=request.user, number=order_number),
        "Checkout_category": order_cart.objects.filter(user=request.user, number=order_number).values_list("category").distinct(),
        "Total": list(order_cart.objects.filter(user=request.user, number=order_number).aggregate(Sum("price")).values())[0],
        "user": request.user,
        "Category": Category.objects.all(),
        "Active_category": category,
        "Menu": menu,
        "Columns": columns,
        "Topping_price": 0.00,
        "Order_number": order_number
    }       
    return render(request,"orders/menu.html", context2)

def delete(request, category, name, price):
    menu, columns=findTable(category)
    order_number=User_order.objects.get(user=request.user, status='On course').order_number
    topping=User_order.objects.get(user=request.user, status='On course')
    if (category == "Regular Pizza" or category == "Sicilian Pizza"):
        if name=="1 topping":
            topping.topping-=1
            topping.save()
        if name=="2 toppings":
            topping.topping-=2
            topping.save()
        if name=="3 toppings":
            topping.topping-=3    
            topping.save()
        topping.topping=0
        topping.save()
        delete_all_toppings=order_cart.objects.filter(user=request.user, category="Toppings")
        delete_all_toppings.delete()
    if category == "Toppings":
        topping.topping+=1
        topping.save()
    find_order=order_cart.objects.filter(user=request.user, category=category, name=name, price=price)[0]
    find_order.delete()  
    context={
        "Checkout": order_cart.objects.filter(user=request.user, number=order_number),
        "Checkout_category": order_cart.objects.filter(user=request.user, number=order_number).values_list("category").distinct(),
        "Total": list(order_cart.objects.filter(user=request.user, number=order_number).aggregate(Sum("price")).values())[0],
        "user": request.user,
        "Category": Category.objects.all(),
        "Active_category": category,
        "Menu": menu,
        "Columns": columns,
        "Topping_price": 0.00,
        "Order_number": order_number
    }       
    return render(request,"orders/menu.html", context)

def my_orders(request, order_number):
    context={
        "Checkout": order_cart.objects.filter(user=request.user, number=order_number),
        "Checkout_category": order_cart.objects.filter(user=request.user, number=order_number).values_list("category").distinct(),
        "Total": list(order_cart.objects.filter(user=request.user, number=order_number).aggregate(Sum("price")).values())[0],
        "user": request.user,
        "Category": Category.objects.all(),
        "Order_number": order_number,
        "All_orders": User_order.objects.filter(user=request.user),
        "Status": User_order.objects.get(user=request.user, order_number=order_number).status
    }
    return render(request, "orders/my_orders.html", context)

def orders_manager(request, user, order_number):
    user=User.objects.get(username=user)
    context={
        "Checkout": order_cart.objects.filter(user=user, number=order_number),
        "Checkout_category": order_cart.objects.filter(user=user, number=order_number).values_list("category").distinct(),
        "Total": list(order_cart.objects.filter(user=user, number=order_number).aggregate(Sum("price")).values())[0],
        "user": request.user,
        "Category": Category.objects.all(),
        "Order_number": order_number,
        "All_orders": User_order.objects.exclude(status="On course")
    }
    return render(request, "orders/orders_manager.html", context)

def complete(request, user, order_number):
    user=User.objects.get(username=user)
    complete=User_order.objects.get(user=user, order_number=order_number)
    complete.status="Completed order"
    complete.save()
    context={
        "Checkout": order_cart.objects.filter(user=user, number=order_number),
        "Checkout_category": order_cart.objects.filter(user=user, number=order_number).values_list("category").distinct(),
        "Total": list(order_cart.objects.filter(user=user, number=order_number).aggregate(Sum("price")).values())[0],
        "user": request.user,
        "Category": Category.objects.all(),
        "Order_number": order_number,
        "All_orders": User_order.objects.exclude(status="On course")
    }
    return render(request, "orders/orders_manager.html", context)

def send(request, order_number):
    status=User_order.objects.get(user=request.user, status="On course")
    status.status="Pending order"
    status.save()
    counter=Order_counter.objects.first()
    new_order_number=User_order(user=request.user, order_number=counter.counter)
    new_order_number.save()
    counter.counter=counter.counter+1
    counter.save()
    return my_orders(request, order_number)

def findTable(category):
    if category=="Regular Pizza":
        menu=regular.objects.all()
        columns=3
    elif category=="Sicilian Pizza":
        menu=sicilian.objects.all()
        columns=3
    elif category=="Toppings":
        menu=toppings.objects.all()
        columns=1
    elif category=="Subs":
        menu=subs.objects.all()
        columns=3
    elif category=="Pasta":
        menu=pasta.objects.all()
        columns=2
    elif category=="Salad":
        menu=salad.objects.all()
        columns=2
    elif category=="Dinner Platters":
        menu=dinner_platter.objects.all()
        columns=3
    return menu, columns