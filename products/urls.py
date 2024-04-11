from django.urls import path
from products import views
from products.views import get_product

urlpatterns = [
    path('<slug>/', get_product, name="get_product"),
    
]
