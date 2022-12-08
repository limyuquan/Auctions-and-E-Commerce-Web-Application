from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Listings)
admin.site.register(Category)
admin.site.register(Wishlist)
admin.site.register(Auction_bids)
admin.site.register(Comments)
# Register your models here.
