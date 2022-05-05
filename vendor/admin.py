from django.contrib import admin
from .models import Vendor, Client, Country, User, Gender

# Register your models here.

admin.site.register(Vendor)
admin.site.register(Country)
admin.site.register(Client)
admin.site.register(User)
admin.site.register(Gender)
