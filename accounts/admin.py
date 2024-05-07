from django.contrib import admin
from .models import Profile
from .models import Cart, CartItems
from django.contrib import admin
from .models import Order, OrderItem
# Register your models here.
admin.site.register(Profile)


admin.site.register(Cart)
admin.site.register(CartItems)



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "created_at", "updated_at")
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
