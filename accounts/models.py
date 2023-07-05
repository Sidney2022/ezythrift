from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
import random
# from core.models import Cart

class Profile(AbstractUser):
    """ custom user model """
    phone_number = models.CharField(max_length=14)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    apartment = models.CharField(max_length=255)

    email = models.EmailField(unique=True)
    # def cart_items(self):
    #     cart = Cart.objects.all()
    #     return cart

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']
    def __str__(self):
        return self.email


class SocialLink(models.Model):
    facebook = models.CharField(max_length=100, blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    linkedin = models.CharField(max_length=100, blank=True)
    instagram = models.CharField(max_length=100, blank=True)


# class Notification(models.Model):
#     user = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     message = models.TextField()
#     icon = models.CharField(max_length=5)
#     color = models.CharField(max_length=10)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def time_sent(self):
#         time_active =   datetime.now().date() - self.timestamp.date()
#         time = float(time_active.total_seconds())   # Return time in secs
#         if time > 3600*24 :
#             time /= (3600*24)
#             msg_time = f"{time} days"
#         elif time > 3600 :
#             time /= 3600
#             msg_time = f"{time} hrs"
#         elif time > 60:
#             time /= 60
#             msg_time = f"{time} mins"
#         else:
#             msg_time = f"{time} secs"
#         return msg_time


