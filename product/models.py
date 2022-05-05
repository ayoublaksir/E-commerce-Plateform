

from django.db import models
from io import BytesIO
# pillow est une libr pour traitement , l'archivage , et l'affichage d'image
from PIL import Image
from django.core.files import File
# pour la representation des fichiers
from django.db.models.lookups import IsNull
from vendor.models import Country, Gender, Vendor, Client

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    ordering = models.IntegerField(default=0)
    description = models.TextField(null=True)

    def get_products_accepted(self):
        return self.products.filter(state="accepted")

    class Meta:
        ordering = ['ordering']

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE)
    vendor = models.ForeignKey(
        Vendor, related_name='product', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)
    country = models.ForeignKey(
        Country, related_name='products', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    state_choices = [("accepted", "accepted"), ("refused",
                                                "refused"), ("pending", "pending")]
    state = models.CharField(max_length=9,
                             choices=state_choices,
                             default="pending")

    def __str__(self):
        return self.title


class Meta:
    ordering = ['-date_added']


class Comment(models.Model):
    titre = models.TextField(blank=True, null=True)

    client = models.ForeignKey(
        Client, related_name='comments', on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(
        Product, related_name='comments', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.titre


class favorite(models.Model):
    client = models.ForeignKey(
        Client, related_name='favorites', on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(
        Product, related_name='favorites', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.product.title)


class Order(models.Model):
    clientusername = models.ForeignKey(
        Client, related_name='orders', on_delete=models.CASCADE, null=True)
    vendorid = models.ForeignKey(
        Vendor, related_name='orders', on_delete=models.SET_NULL, null=True)

    productid = models.ForeignKey(
        Product, related_name='orders', on_delete=models.SET_NULL, null=True)
    country = models.ForeignKey(
        Country, related_name='orders', on_delete=models.SET_NULL, null=True)
    gender = models.ForeignKey(
        Gender, related_name='orders', on_delete=models.SET_NULL, null=True)

    slug = models.SlugField(max_length=255)
    quantity = models.IntegerField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    price=models.IntegerField(null=True)

    def __str__(self):
        return str(self.clientusername)
