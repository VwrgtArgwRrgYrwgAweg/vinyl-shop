from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import models
from .models import Product, Order, OrderItem
from .cart import Cart

def home(request):
    products = Product.objects.all()
    search_query = request.GET.get('search', '')
    
    if search_query:
        products = products.filter(
            models.Q(title__icontains=search_query) |
            models.Q(artist__icontains=search_query)
        )
    
    products = products[:12]
    return render(request, 'main/home.html', {
        'products': products,
        'search_query': search_query
    })

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'main/cart.html', {'cart': cart})

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product)
    return redirect('cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

def checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        comment = request.POST.get('comment', '')
        
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            comment=comment,
            total=cart.get_total_price()
        )
        
        for item in cart:
            product = item['product']
            quantity = item['quantity']
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=item['price']
            )
            product.stock -= quantity
            product.save()
        
        cart.clear()
        return JsonResponse({'status': 'ok', 'order_id': order.id})
    
    return render(request, 'main/checkout.html', {'cart': cart})

def delivery(request):
    return render(request, 'main/delivery.html')

def about(request):
    return render(request, 'main/about.html')

def contacts(request):
    return render(request, 'main/contacts.html')