import stripe
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Product, Cart, CartItem, Order
from .chatbot import chatbot_response

stripe.api_key = settings.STRIPE_SECRET_KEY

def base(request):
    products = Product.objects.all()
    return render(request, 'store/base.html', {'products': products})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.exclude(pk=pk)[:4]
    return render(request, 'store/product_detail.html', {'product': product, 'related_products': related_products})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1 if not item_created else 0
    cart_item.save()
    return redirect('store:cart_details')

@login_required
def cart_details(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.items.exists():
        return render(request, 'store/cart_details.html', {'message': "Your cart is empty."})
    total_price = sum(item.product.price * item.quantity for item in cart.items.all())
    return render(request, 'store/cart_details.html', {'cart': cart, 'total_price': total_price})

@login_required
def fake_checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('store:cart_details')

    line_items = [
        {
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': item.product.name},
                'unit_amount': int(item.product.price * 100),
            },
            'quantity': item.quantity,
        }
        for item in cart.items.all()
    ]

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri(reverse('store:checkout_success')),
            cancel_url=request.build_absolute_uri(reverse('store:checkout_cancel')),
        )
        return JsonResponse({'id': checkout_session.id})
    except Exception as e:
        messages.error(request, "Payment failed. Please try again.")
        return redirect('store:cart_details')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('store:login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    next_url = request.GET.get('next', 'store:product_list')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'store/login.html', {'next': next_url})

def chatbot_reply(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message")
        bot_response = chatbot_response(user_message)
        return JsonResponse({"response": bot_response})
    return JsonResponse({"error": "Invalid request"}, status=400)

def checkout_success(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        Order.objects.create(user=request.user, items=cart.items.all())
        cart.items.all().delete()  # Clear cart items after the order is placed
    
    messages.success(request, "Thank you for your purchase!")
    return render(request, 'store/checkout_success.html')

def checkout_cancel(request):
    return render(request, 'store/checkout_cancel.html')
