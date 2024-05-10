from django.shortcuts import render, redirect
from accounts.views import cart
from products.models import *


# Create your views here.

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from products.models import Product


    
    

def get_product(request, slug):
    try:
        # Retrieve the product by its slug or return a 404 error if not found
        product = get_object_or_404(Product, slug=slug)  # Example condition
        context = {'product': product}

        # Check if there's a 'size' parameter in the GET request
        if request.GET.get('size'):
            size = request.GET.get('size')
            price = product.get_product_price_by_size(size)
            context['selected_size'] = size
            context['updated_price'] = price

        # Check if there's a 'color' parameter in the GET request
        if request.GET.get('color'):
            color = request.GET.get('color')
            image = product.get_product_image_by_color(color)
            context['selected_color'] = color
            context['updated_image'] = image

        # Return the rendered template with context
        return render(request, 'product/product.html', context)

    except Product.DoesNotExist:
        # Return a 404 error if the product isn't found
        raise Http404("Product not found")

    except Exception as e:
        # Log the error and return a generic error message
        # Optionally, you can use a logger instead of print for production
        print("An error occurred in get_product:", e)
        return HttpResponse("An error occurred", status=500)

        
from django.shortcuts import render
from django.db.models import Q
from products.models import Product

def search_products(request):
    query = request.GET.get('q', '')  # Retrieve the search query
    context = {'query': query, 'results': []}  # Initialize with default values

    if query:
        search_terms = query.split()  # Split query into words
        query_filter = Q()

        # Build a query filter to find matching products
        for term in search_terms:
            query_filter |= (
                Q(product_name__icontains=term) |
                Q(product_description__icontains=term)
            )

        # Fetch matching products
        products = Product.objects.filter(query_filter).distinct()
        context['results'] = products  # Pass to context
    
    # Render the search results template
    return render(request, 'product/search_results.html', context)
