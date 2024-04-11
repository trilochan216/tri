from django.contrib import admin

# Register your models here.
from.models import *

admin.site.register(Category)
admin.site.register(Coupon)

class ProductImangeAdmin(admin.StackedInline):
    model = ProductImage
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'price']
    inlines = [ProductImangeAdmin]
    
@admin.register(ColorVariant)
class ColorvariantAdmin(admin.ModelAdmin):
    list_display =['color_name', 'price']
    model = ColorVariant
    
@admin.register(SizeVariant)
class SizeVariantAdmin(admin.ModelAdmin):
    list_display =['size_name', 'price']
    model = SizeVariant
       

admin.site.register(Product, ProductAdmin)



admin.site.register(ProductImage)