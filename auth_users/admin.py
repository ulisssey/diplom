from django.contrib import admin
from .models import Item, Categories, Watchlist, CartItem


admin.site.register(Item)
admin.site.register(Categories)
admin.site.register(Watchlist)
admin.site.register(CartItem)
