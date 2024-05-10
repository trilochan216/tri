from django.urls import path
from products import views
from products.views import get_product, search_products

urlpatterns = [
    path('<slug>/', get_product, name="get_product"),
    path('product/search/', search_products, name='search-products'),
    
]
