 

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
