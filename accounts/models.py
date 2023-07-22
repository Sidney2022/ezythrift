from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
import random


class Profile(AbstractUser):
    """ custom user model """

    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']
    def __str__(self):
        return self.email
    
    def billing_address(self):
        if Billing.objects.filter(user=self.id).exists():
            return Billing.objects.filter(user=self.id).first()
        else:
            return False


class Billing(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    apartment = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=14)


