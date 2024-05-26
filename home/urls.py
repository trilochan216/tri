from django.urls import path
from home.views import about, contact, index, product
from . import views

urlpatterns = [
    path('', index, name="index"),
    path('products/', product, name="product"),
    path('About-us/', about, name="about"),
    path('Contact/', contact, name="contact"),
]

