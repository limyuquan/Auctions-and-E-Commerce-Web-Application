from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

#auction listings, bids, comments, and auction categories
#one for auction listings, one for bids, and one for comments made on auction listings.

class User(AbstractUser):
    pass

class Category(models.Model):
    category_name = models.CharField(max_length=64)
    
    def __str__(self):
        return self.category_name
    
class Listings(models.Model):
    title = models.CharField(max_length=64)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    description = models.CharField(max_length=500)
    imageURL = models.CharField(max_length=1000)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category", null=True, blank=True )
    isActive = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title 
    
class Auction_bids(models.Model):
    item = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="item")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    bid = models.DecimalField(decimal_places=2, max_digits=10)
    def __str__(self):
        return f"{self.item}, {self.bidder}, {self.bid}" 
    
class Comments(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter", default=None)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="commentItem", default=None)
    comment = models.CharField(max_length=300, default=None)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    time = models.TimeField(default=datetime.now())

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wisher")
    item = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="wishItem", default=None)
    