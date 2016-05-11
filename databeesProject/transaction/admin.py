from django.contrib import admin
from .models import Auction, BuyItNow, SaleResult

admin.site.register(Auction)
admin.site.register(BuyItNow)
admin.site.register(SaleResult)