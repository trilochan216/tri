from django.db import models
from base.models import BaseModel
from django.utils.text import slugify

# Create your models here.

class Category(BaseModel):
    app_label = 'lugga'
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category_image = models.ImageField(upload_to="categories")
    
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)
        
    
    def __str__(self) -> str:
        return self.category_name

class ColorVariant(BaseModel):
    color_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    image = models.ImageField(default = True)
    
    def __str__(self) -> str:
        return self.color_name
        

class SizeVariant(BaseModel):
    size_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    
    
    def __str__(self) -> str:
        return self.size_name
       

class Product(BaseModel):
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    price = models.IntegerField()
    product_description = models.TextField()
    color_variant = models.ManyToManyField(ColorVariant, blank=True)
    size_variant = models.ManyToManyField(SizeVariant, blank=True)
        # Adding a stock field to manage product inventory
    stock = models.PositiveIntegerField(default=0)
    
    
    def save(self, *args, **kwargs):
            if not self.slug or self.slug == "":
                base_slug = slugify(self.product_name)
                unique_slug = base_slug
                counter = 1

                # Loop until a unique slug is found
                while Product.objects.filter(slug=unique_slug).exists():
                    unique_slug = f"{base_slug}-{counter}"
                    counter += 1

                self.slug = unique_slug

            super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.product_name
    
    
    def get_product_price_by_size(self, size):
        return self.price + SizeVariant.objects.get(size_name = size).price
    
    
    def get_product_image_by_color(self, color):
        color_variant = self.color_variant.filter(color_name=color).first()
        if color_variant:
            return color_variant.image
        


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")
    image = models.ImageField(upload_to="product")
    

class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=100 )
    minimum_amount = models.IntegerField(default=2000)
