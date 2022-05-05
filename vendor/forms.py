from vendor.models import User, Vendor
from django.forms import ModelForm
from product.models import Product
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import Client, Gender, Vendor, Country


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'image', 'title', 'description', 'price']


class VendorInscriptionForm(UserCreationForm):

    phone_number = forms.IntegerField(required=True)
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(), required=True)
    gender = forms.ModelChoiceField(
        queryset=Gender.objects.all(), required=True)
    email = forms.EmailField(max_length=254, required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_vendor = True
        user.save()
        vendor = Vendor.objects.create(user=user, username=user.username)
        vendor.phone_number = self.cleaned_data.get('phone_number')
        vendor.country = self.cleaned_data.get('country')
        vendor.gender = self.cleaned_data.get('gender')
        vendor.email = self.cleaned_data.get('email')
        vendor.first_name = self.cleaned_data.get('first_name')
        vendor.last_name = self.cleaned_data.get('last_name')

        vendor.save()
        return user


class ClientInscriptionForm(UserCreationForm):

    phone_number = forms.IntegerField(required=True)
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(), required=True)
    gender = forms.ModelChoiceField(
        queryset=Gender.objects.all(), required=True)
    email = forms.EmailField(max_length=254, required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_client = True
        user.save()
        client = Client.objects.create(user=user, username=user.username)
        client.location = self.cleaned_data.get('location')
        client.phone_number = self.cleaned_data.get('phone_number')
        client.country = self.cleaned_data.get('country')
        client.gender = self.cleaned_data.get('gender')
        client.email = self.cleaned_data.get('email')
        client.first_name = self.cleaned_data.get('first_name')
        client.last_name = self.cleaned_data.get('last_name')
        client.save()
        return user
