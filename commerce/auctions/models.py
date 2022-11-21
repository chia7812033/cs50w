from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)

class Item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=19, decimal_places=10)
    create_date = models.DateField(auto_now=False, auto_now_add=True)
    create_time = models.TimeField(auto_now=False, auto_now_add=True)
    description = models.TextField()
    image = models.ImageField(upload_to="items/")
    
