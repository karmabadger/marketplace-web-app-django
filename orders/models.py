from django.db import models
from django.contrib.auth.models import User
from listings.models import Listing

# Create your models here.

class CartEntry(models.Model):
    listing    = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity   = models.PositiveIntegerField()
    ordered    = models.BooleanField(default=False)

    def get_total_price(self):
            total_price = 0
            entries = CartEntry.objects.filter(ordered=False)
            for e in entries:
                total_price += (e.listing.money_price * e.quantity)
            return total_price

class Order(models.Model):
    user_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    listings = models.ManyToManyField(Listing)

class OrderHistory(models.Model):
    checkout_user = models.ForeignKey(User, on_delete=models.CASCADE)
    orders = models.ForeignKey(CartEntry, on_delete=models.CASCADE)