from django.shortcuts import render
from products.models import Product

# Create your views here.
def index(request):
    context = {'products': Product.objects.all()}
    return render(request, 'home/index.html', context)

def product(request):
    context = {'products': Product.objects.all()}
    return render(request, 'home/products.html', context)

def about(request):
  
    return render(request, 'home/about.html')

def contact(request):

    return render(request, 'home/contact.html')