from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cart.models import CartItem
from .models import Order, OrderItem

def checkout(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart_items = CartItem.objects.filter(session_key=request.session.session_key)
    
    if not cart_items:
        messages.warning(request, "Savat bo'sh!")
        return redirect('cart')
    
    total = sum(item.total_price for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'orders/checkout.html', context)

def place_order(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user)
        else:
            cart_items = CartItem.objects.filter(session_key=request.session.session_key)
        
        if not cart_items:
            messages.error(request, "Savat bo'sh!")
            return redirect('cart')
        
        total = sum(item.total_price for item in cart_items)
        
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=request.POST.get('full_name'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city', 'Toshkent'),
            total_amount=total,
        )
        
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        
        cart_items.delete()
        
        messages.success(request, f"Buyurtma #{order.id} muvaffaqiyatli yaratildi!")
        return redirect('order_success', order_id=order.id)
    
    return redirect('checkout')

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {'order': order}
    return render(request, 'orders/order_success.html', context)

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {'orders': orders}
    return render(request, 'orders/my_orders.html', context)