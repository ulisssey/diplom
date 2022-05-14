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


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    apartment = models.CharField(max_length=100)
    default = models.BooleanField(default=False)


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} - {self.item.title}"

    def get_total_price(self):
        return self.quantity * self.item.price


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_price()
        return total


class Watchlist(models.Model):
    watchlist = models.CharField(max_length=200, null=True, blank=True)
    author_id = models.CharField(max_length=50, null=True)
