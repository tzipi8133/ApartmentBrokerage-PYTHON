from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Person, Seller, Appartment, Request

# Register your models here.
admin.site.register(Person)
admin.site.register(Seller)
admin.site.register(Appartment)
admin.site.register(Request)
