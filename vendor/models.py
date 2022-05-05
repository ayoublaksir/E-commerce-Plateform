from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    is_client = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)


class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Gender(models.Model):
    gender = models.CharField(max_length=100)

    def __str__(self):
        return self.gender


class Vendor(models.Model):
    user = models.OneToOneField(
        User, related_name='vendor', on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, related_name='vendors')
    phone_number = models.IntegerField(null=True)
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.username


class Client(models.Model):
    user = models.OneToOneField(
        User, related_name='client', on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=100, null=True)
    phone_number = models.IntegerField(null=True)
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, related_name='clients')
    email = models.EmailField(max_length=254, null=True)
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.username
