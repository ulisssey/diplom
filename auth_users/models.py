from django.db import models
from django.contrib.auth.models import User


class Categories(models.Model):
    categories = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.categories


class Item(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')
    price = models.IntegerField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True, default='Nothing')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.description[:50]


class Watchlist(models.Model):
    watchlist = models.CharField(max_length=200, null=True, blank=True)
    author_id = models.CharField(max_length=50, null=True)


class CartItem(models.Model):
    cart_item = models.CharField(max_length=200, null=True, blank=True)
    author_id = models.CharField(max_length=50, null=True)
