from django.shortcuts import render, redirect
from accounts.views import cart
from products.models import *


# Create your views here.

def get_product(request, slug):
    
    print("*******")
    print(request.user)
    print("*******")
    print(request.user.profile.get_cart_count)
    try:
        product = Product.objects.get(slug =slug)
        context = {'product': product}
        if request.GET.get('size'):
            size = request.GET.get('size')
            price = product.get_product_price_by_size(size)
            context['selected_size'] = size
            context['updated_price'] = price
            print(price)
        
        if request.GET.get('color'):
            color = request.GET.get('color')
            image = product.get_product_image_by_color(color)
            context['selected_color'] = color
            context['updated_image'] = image
            print(image)
        
        return render(request, 'product/product.html' , context= context)
    
    except Exception as e:
        print("the error is :")
        print(e)


           