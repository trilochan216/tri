from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.emails import send_account_activation_email
from products.models import Coupon, Product, ColorVariant, SizeVariant
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from enum import Enum
from django.apps import apps
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django import forms
# Create your models here.

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile')
    

    def get_cart_count(self):
        return CartItems.objects.filter(cart__is_paid=False, cart__user=self.user).count()


class Cart(models.Model):  
    # Combining both customer and user relationships
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')  # Ensuring unique relationship
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(default= 0)   # Merging total field
    is_paid = models.BooleanField(default=False)  # Keeping is_paid field
    created_at = models.DateTimeField(auto_now_add=True)   # Date when cart was created
    
    # Method to calculate the total cart value
    def get_cart_total(self):
        cart_items = self.cart_items.all()
        price = []
        for cart_item in cart_items:
            price.append(cart_item.product.price)
            if cart_item.color_variant:
                price.append(cart_item.color_variant.price)
            if cart_item.size_variant:
                price.append(cart_item.size_variant.price)
        
        # Applying coupon discount if applicable
        if self.coupon and self.coupon.minimum_amount < sum(price):
            return sum(price) - self.coupon.discount_price
        
        return sum(price)
    
    def __str__(self):
        return f"Cart: {self.id} (User: {self.user.username if self.user else 'None'})"

    

class CartItems(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # Ensures unique identifier
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='cart_items')  # Ensure 'Cart' is defined
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    color_variant = models.ForeignKey(ColorVariant, on_delete=models.SET_NULL, null= True, blank=True )
    size_variant = models.ForeignKey(SizeVariant, on_delete=models.SET_NULL, null= True, blank=True )
    quantity = models.PositiveIntegerField(default=1)
    
    def get_product_price(self):
        price = [self.product.price]
        
        if self.color_variant:
            color_variant_price = self.color_variant.price
            price.append(color_variant_price)
        if self.size_variant:
            size_variant_price = self.size_variant.price
            price.append(size_variant_price)
        
        return sum(price)
    
    def get_product_price(self):
        return self.product.price * self.quantity  # A method to get total price for this item

# Create your models here.


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="admins")
    mobile = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, null=True, blank=True)
    joined_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products")
    marked_price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField()
    description = models.TextField()
    warranty = models.CharField(max_length=300, null=True, blank=True)
    return_policy = models.CharField(max_length=300, null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/images/")

    def __str__(self):
        return self.product.title


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return "Cart: " + str(self.cart.id) + " CartProduct: " + str(self.id)




    

@receiver(post_save, sender = User) 
def send_email_token(sender, instance, created, **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            Profile.objects.create(user= instance, email_token= email_token)
            email = instance.email
            send_account_activation_email(email, email_token)
            
    except Exception as e:
        print(e)
        
        

# Enum for Order Status
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.translation import gettext_lazy as _

# Enum for Order Status
class OrderStatus(models.TextChoices):
    PROCESSING = "Processing", _("Processing")
    COMPLETED = "Completed", _("Completed")
    CANCELED = "Canceled", _("Canceled")

# Order model
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.TextField()
    payment_method = models.CharField(
        max_length=20, 
        default="Cash on Delivery"
    )
    status = models.CharField(
        max_length=10, 
        choices=OrderStatus.choices, 
        default=OrderStatus.PROCESSING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.pk} - {self.name} - {self.status}"

    # Method to calculate the total revenue from completed orders
    @classmethod
    def total_revenue(cls):
        return sum(order.total_price() for order in cls.objects.filter(status=OrderStatus.COMPLETED))

    # Method to count all completed orders
    @classmethod
    def total_completed_orders(cls):
        return cls.objects.filter(status=OrderStatus.COMPLETED).count()

    # Calculate the total price for an order
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())



# OrderItem model
from django.db import models
from products.models import Product  # Make sure this import is correct

class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.product_name} x {self.quantity}"



from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, OrderStatus, OrderItem

@receiver(post_save, sender=Order)
def handle_order_status_change(sender, instance, created, **kwargs):
    if not created and instance.status == "Completed":
        for item in instance.items.all():
            product = item.product
            if product.stock < item.quantity:  # Ensure stock doesn't go negative
                raise ValueError("Insufficient stock")
            product.stock -= item.quantity
            product.save()


