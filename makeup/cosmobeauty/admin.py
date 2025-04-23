from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomUser)
 
admin.site.register(Category)

admin.site.register(Brands)

admin.site.register(Products)

admin.site.register(Cart)

admin.site.register(Wishlist)

admin.site.register(Order)

admin.site.register(Billing)