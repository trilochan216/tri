from django.contrib import admin

from customadmin.models import Seller

# Register your models here.
from django.contrib import admin
from .models import Seller

class SellerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address', 'is_verified')

admin.site.register(Seller, SellerAdmin)
