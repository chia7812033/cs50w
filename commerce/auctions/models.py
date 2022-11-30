from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)


class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=19, decimal_places=10)
    create_date = models.DateField(auto_now=False, auto_now_add=True)
    create_time = models.TimeField(auto_now=False, auto_now_add=True)
    description = models.TextField()
    imageURL = models.URLField(max_length=200)
    createby = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listing")

    def __str__(self):
        return self.title

class Bid(models.Model):
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bid")
    bid = models.DecimalField(max_digits=19, decimal_places=10)

class WatchList(models.Model):
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_watch")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watch")

class Comment(models.Model):
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comment")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")
    comment = models.TextField()

