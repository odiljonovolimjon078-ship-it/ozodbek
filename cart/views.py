from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product
from .models import CartItem

def cart_view(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart_items = CartItem.objects.filter(session_key=request.session.session_key)
    
    total = sum(item.total_price for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'cart/cart.html', context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user, 
            product=product
        )
    else:
        if not request.session.session_key:
            request.session.create()
        cart_item, created = CartItem.objects.get_or_create(
            session_key=request.session.session_key, 
            product=product
        )
    
    cart_item.quantity += 1
    cart_item.save()
    
    messages.success(request, f"{product.name} savatga qo'shildi!")
    return redirect('product_list')