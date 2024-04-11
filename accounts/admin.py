from django.contrib import admin
from .models import Profile
from .models import Cart, CartItems
# Register your models here.
admin.site.register(Profile)


admin.site.register(Cart)
admin.site.register(CartItems)
