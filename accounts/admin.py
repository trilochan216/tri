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


admin.site.register(OrderItem)

from django.contrib import admin
from .models import Order, OrderStatus, OrderItem

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at', 'updated_at')
    list_editable = ('status',)  # Allow inline editing of the status
    list_filter = ('status',)
    search_fields = ('user__username',)

admin.site.register(Order, OrderAdmin)



