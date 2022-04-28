from django.db import models


class Categories(models.Model):
    categories = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.categories


class Item(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')
    price = models.IntegerField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.description[:50]
