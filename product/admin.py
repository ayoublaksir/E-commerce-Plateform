from django.contrib import admin
from .models import Category, Product, Order, Comment, favorite

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Comment)
admin.site.register(favorite)
# Register your models here.
