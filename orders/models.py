from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('processing', 'Tayyorlanmoqda'),
        ('shipped', 'Yuborildi'),
        ('delivered', 'Yetkazildi'),
        ('cancelled', 'Bekor qilindi'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100, default="Toshkent")
    total_amount = models.DecimalField(max_digits=12, decimal_places=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Buyurtma #{self.id} - {self.full_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"