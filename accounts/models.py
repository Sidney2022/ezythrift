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
    
    def is_billing_address(self):
        if Billing.objects.filter(user=self.id).exists():
            return True
        else:
            return False
    def billing(self):
        return Billing.objects.filter(user=self.id).first()


class SocialLink(models.Model):
    facebook = models.CharField(max_length=100, blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    linkedin = models.CharField(max_length=100, blank=True)
    instagram = models.CharField(max_length=100, blank=True)


class Billing(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=14)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    apartment = models.CharField(max_length=255)


