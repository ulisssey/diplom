from django.contrib import admin
from .models import Item, Categories, Watchlist, OrderItem, Order, Address


admin.site.register(Item)
admin.site.register(Categories)
admin.site.register(Watchlist)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Address)
