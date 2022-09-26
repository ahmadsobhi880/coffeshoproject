import json
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from coffee_app.models import Coffee, Order, OrderItem
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from users.decorators import allowed_users

# Create your views here.

class CartView(View):
    def get(self, request):
        cart = request.session.get("cart", {})
        if not cart:
            request.session["cart"] = {}
        data = []
        total_price = 0
        if cart:
            products = Coffee.get_coffee_by_id(cart.keys())
            for product in products:
                quantity = cart.get(str(product.id), None)
                if quantity:
                    product_total = product.price * int(quantity)
                    data.append({
                        "product": product,
                        "quantity": quantity,
                        "total_price": product_total
                    })
                    total_price += product_total
        context = {"data": data, "total_price": total_price}
        return render(request, "store/cart.html", context)

    def post(self, request):
        product_id = request.POST.get('product_id', None)
        action = request.POST.get('action', None)
        cart = request.session.get('cart', {})
        if not cart:
            cart = request.session["cart"] = {}

        quantity = cart.get(product_id, None)

        if quantity:
            if action == "remove":
                if quantity <= 1:
                    cart.pop(product_id)
                    messages.success(request, "Item Removed")
                else:
                    cart[product_id] = quantity-1
                    messages.success(request, "Quantity Decreased")
            elif action == "add":
                cart[product_id] = quantity+1
                messages.success(request, "Quantity Increased")
            elif action == "delete":
                cart.pop(product_id)
                messages.success(request, "Item Removed")
        else:
            cart[product_id] = 1
            messages.success(request, "Added to cart successfully.")

        request.session['cart'] = cart
        
        print('cart', request.session['cart'])
        previous_url = request.META['HTTP_REFERER'] 
        if previous_url:
            return redirect(previous_url)
        return redirect('store:HomeView')

class AllOrdersView(View):
    @allowed_users(allowed_roles=["bariast"])
    def get(self, request):
        try:
            orders = request.user.orders.all().order_by("-date")
        except:
            orders = None
        context = {"orders": orders}
        return render(request, "store/list-all-orders.html", context)


class MyOrders(View):
    def get(self, request):
        try:
            orders = request.user.orders.all().order_by("-date")
        except:
            orders = None
        context = {"orders": orders}
        return render(request, "store/my-orders.html", context)


@method_decorator(csrf_exempt,  name='dispatch')
class CheckOutView(View):
    def post(self, request):
        user = request.user
        cart = request.session.get("cart", {})
        order_items = []
        total_price = 0
        products = Coffee.get_coffee_by_id(cart.keys())
        for product in products:
            quantity = cart.get(str(product.id), None)
            if quantity:
                product_total = product.price * int(quantity)
                order_item = OrderItem.objects.create(
                    item = product,
                    price = product_total,
                    quantity = quantity,
                )
                order_items.append(order_item)
                total_price += product_total
        order = Order.objects.create(
            customer = user,
            price = total_price,
            status = 'c',
        )
        for item in order_items:
            order.items.add(item)
        request.session["cart"] = None
        return HttpResponse(status=200)
