# customadmin/forms.py
from django import forms
from products.models import Product, ProductImage
from django.forms import modelformset_factory

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'category', 'price', 'product_description', 'stock']

# Formset for handling multiple product images
ProductImageFormSet = modelformset_factory(
    ProductImage,
    fields=['image'],
    extra=3,  # Allow 3 additional image uploads by default
    can_delete=True  # Allow deleting images from the formset
)
