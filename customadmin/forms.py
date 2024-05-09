# customadmin/forms.py
from django import forms
from products.models import Product, ColorVariant, SizeVariant, ProductImage
from django.forms import modelformset_factory

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'category', 'price', 'product_description', 'stock']

from django.forms import modelformset_factory
from products.models import ColorVariant, SizeVariant, ProductImage

# Formset for color variants
ColorVariantFormSet = modelformset_factory(
    ColorVariant,
    fields=['color_name', 'price', 'image'],  # Include optional fields
    extra=1,  # Allows one empty form by default
    can_delete=True  # Allow deletion
)

# Formset for size variants
SizeVariantFormSet = modelformset_factory(
    SizeVariant,
    fields=['size_name', 'price'],
    extra=1,  # Allows one empty form by default
    can_delete=True
)

# Formset for product images
ProductImageFormSet = modelformset_factory(
    ProductImage,
    fields=['image'],  # Field for image uploads
    extra=3,  # At least one empty form to start with
    can_delete=True
)
