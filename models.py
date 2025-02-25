from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings
class Account(AbstractUser):
    phono = models.CharField(max_length=15, default='default_value', null=False)
    address = models.CharField(max_length=255)


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image=models.ImageField(upload_to='images/')
    def __str__(self):
        return self.name
class MedicationInfo(models.Model):
    name = models.CharField(max_length=100)
    uses = models.TextField()
    composition = models.TextField()
    mechanism_of_action = models.TextField()
    contraindications = models.TextField()
    side_effects = models.TextField()
    usage_instructions = models.TextField()
    image = models.ImageField(upload_to='medications/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    total_price=models.DecimalField(max_digits=10,decimal_places=2)
    status=models.CharField(max_length=50,default='Pending')
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order #{self.id}-{self.status}"
    
class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.ForeignKey(MedicationInfo,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
class Cart(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(MedicationInfo, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"  
