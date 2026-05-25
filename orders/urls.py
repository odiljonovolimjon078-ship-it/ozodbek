from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('success/<int:order_id>/', views.order_success, name='order_success'),
    path('my-orders/', views.my_orders, name='my_orders'),
]