 

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city = models.TextField(blank=True)
    state = models.TextField(blank=True)

    def __str__(self):
        return self.username

class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    code = models.CharField(max_length=6)
    purpose = models.CharField(max_length=20, choices=[('register', 'Register')])
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"
    
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"