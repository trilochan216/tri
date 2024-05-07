from django.forms import SlugField
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.decorators import login_required
from products.models import *
from accounts.models import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Order, OrderItem, Cart, CartProduct
from django.shortcuts import render, get_object_or_404
from .models import Order, OrderItem
from accounts.models import Cart
from products.models import Product
from django.views.decorators.http import require_POST
from accounts.forms import CheckoutForm
   
    
# Create your views here.
def login_page(request):
     
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user_obj = User.objects.filter(username= email)
        
        
        if not user_obj.exists():
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)
        
        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, 'your account is not verified. ')
            return HttpResponseRedirect(request.path_info)
        
        user_obj = authenticate(username= email, password= password)
        if user_obj:
            login(request, user_obj)
            return redirect('/')
        
        
        messages.warning(request, "Invalid credentials. ")
        return HttpResponseRedirect(request.path_info)
    
    return render(request, 'accounts/login.html')
    

def register_page(request):
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user_obj = User.objects.filter(username= email)
        
        
        if user_obj.exists():
            messages.warning(request, 'Email is already taken. ')
            return HttpResponseRedirect(request.path_info)
        
        
        
        user_obj = User.objects.create(first_name=first_name, last_name=last_name, email=email, username=email)
        user_obj.set_password(password)
        user_obj.save()
        
        
        messages.success(request, "An Email has been sent on your mail. ")
        return HttpResponseRedirect(request.path_info)
    return render(request, 'accounts/register.html')


def activate_email(request, email_token):
    try:
        user = Profile.objects.get(email_token= email_token)
        user.is_email_verified = True
        user.save()
        return redirect('/')
    except Exception as e:
        return HttpResponse('Invalid Email token')
    
 
@login_required
def add_to_cart(request, slug):
    # Do not reassign the slug variable
    product = get_object_or_404(Product, slug=slug)  # Use the slug from the URL parameter
    user = request.user
    cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)

    cart_item = CartItems.objects.create(cart=cart, product=product)

    variant = request.GET.get('variant')  # Fetch variant from the request
    if variant:
        size_variant = SizeVariant.objects.get(size_name=variant)
        cart_item.size_variant = size_variant
        cart_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_cart(request, cart_item_uid):
    try:
        cart_item = CartItems.objects.get(uid =cart_item_uid)
        cart_item.delete()
    except Exception as e:
        print(e)
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    
# def cart(request):
#     context = {'cart': Cart.objects.filter(is_paid=False, user= request.user)}
#     if request.method == 'POST':
#         pass
#     return render(request, 'accounts/cart.html' , context)

@login_required
def cart(request):
    # Safely get the first unpaid cart for the current user
    cart_obj = Cart.objects.filter(is_paid=False, user=request.user).first()  # No exception if no cart
    
    if not cart_obj:
        # Handle case when no unpaid cart exists
        # Example: Create a new cart or return an appropriate response
        messages.warning(request, "No active cart found.")
        return HttpResponseRedirect("/")  # Redirect to home or another appropriate page
    
    cart_items = cart_obj.cart_items.all()  # Get all items in the cart
    cart_total = cart_obj.get_cart_total()  # Get the total price of the cart
    
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart_obj': cart_obj,
    }
    
    # Additional logic (e.g., applying coupons, etc.)
    if not cart_obj:
    # Create a new cart for the user if none exists
        cart_obj = Cart.objects.create(user=request.user, is_paid=False)
    
    # You might want to add this to the context
        cart_items = []
        cart_total = 0
    
        messages.info(request, "A new cart has been created.")
    
    if request.method == 'POST':
        coupon = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(coupon_code__icontains = coupon)
        
        if not coupon_obj.exists():
            messages.warning(request, 'Invalid Coupon.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if cart_obj.coupon:
            messages.warning(request, 'coupon already exists.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))   
        
        if cart_obj.get_cart_total() < coupon_obj[0].minimum_amount:
            messages.warning(request, f'Amount should be greated then {coupon_obj[0].minimum_amount}.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        
        if coupon_obj[0].is_expired:
            messages.warning(request, "coupon Expired")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))    
        
        cart_obj.coupon = coupon_obj[0]
        cart_obj.save()
        messages.success(request, 'coupon applied.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))   
        
    return render(request, 'accounts/cart.html', context)


def remove_coupon(request, cart_id):
    cart = Cart.objects.get(uid = cart_id)
    cart.coupon = None
    cart.save()
    messages.success(request, 'coupon Removed.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 




# @login_required
# def checkout(request):
#     if request.method == 'POST':
#         # Extract data from the form
#         address = request.POST.get("address")
#         payment_method = request.POST.get("payment_method")

#         # Retrieve the user's cart
#         cart = Cart.objects.get(customer=request.user.customer, is_paid=False)
#         total_cost = sum(item.subtotal for item in cart.cartproduct_set.all())

#         # Create a new order with the payment method
#         order = Order.objects.create(
#             user=request.user,
#             total_cost=total_cost,
#             payment_method=payment_method,
#             address=address,
#         )

#         # Create OrderItem for each item in the cart
#         for cart_product in cart.cartproduct_set.all():
#             OrderItem.objects.create(
#                 order=order,
#                 product=cart_product.product,
#                 quantity=cart_product.quantity,
#                 price=cart_product.subtotal,
#             )

#         # Mark the cart as paid
#         cart.is_paid = True
#         cart.save()

#         # Redirect to eSewa payment if chosen
#         if payment_method == "Esewa":
#             return redirect(f"/esewa-request/?o_id={order.id}")

#         # Otherwise, redirect to order detail page
#         return redirect("order_detail", order_id=order.id)

#     # Default behavior if request is not POST
#     return redirect("cart")


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "order_detail.html", {"order": order})



# import requests # type: ignore
# from django.views import View
# from django.shortcuts import render, redirect
# from django.conf import settings
# from django.http import JsonResponse
# from .models import Order
# import xml.etree.ElementTree as ET

# # View to initiate eSewa payment
# class EsewaRequestView(View):
#     def get(self, request, *args, **kwargs):
#         o_id = request.GET.get("o_id")
#         order = Order.objects.get(id=o_id)
#         context = {
#             "order": order,
#             # "esewa_merchant_code": "EPAYTEST",
#             "esewa_return_url": "https://esewa.com.np",
#             "esewa_failure_url": "https://google.com",
#         }
#         return render(request, "esewarequest.html", context)

# # View to verify eSewa payment
# class EsewaVerifyView(View):
#     def get(self, request, *args, **kwargs):
#         o_id = request.GET.get("oid")
#         amt = request.GET.get("amt")
#         refId = request.GET.get("refId")

#         # Configuration for eSewa verification
#         url = "https://uat.esewa.com.np/epay/transrec"
#         data = {
#             'amt': amt,
#             'scd': 'EPAYTEST',
#             'rid': refId,
#             'pid': o_id,
#         }
#         response = requests.post(url, data)
#         root = ET.fromstring(response.content)
#         status = root[0].text.strip()

#         order_obj = Order.objects.get(id=o_id.split("_")[1])

#         if status == "Success":
#             order_obj.payment_completed = True
#             order_obj.payment_reference = refId
#             order_obj.save()
#             return redirect("/")
#         else:
#             return redirect("/esewa-request/?o_id=" + str(order_obj.id))
        
        

from django import forms

class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    address = forms.CharField(widget=forms.Textarea)
    payment_method = forms.ChoiceField(
        choices=[("Cash on Delivery", "Cash on Delivery")],  # Ensure this exists
        required=True  # Ensure the field is required
    )

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Order, OrderItem, CartItems, Cart
from .forms import CheckoutForm

@login_required
def checkout(request):
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Create the order
                order = Order.objects.create(
                    user=request.user,
                    name=form.cleaned_data['name'],
                    email=form.cleaned_data['email'],
                    address=form.cleaned_data['address'],
                    payment_method="Cash on Delivery"
                )
                
                # Add order items from the cart
                cart = Cart.objects.filter(user=request.user, is_paid=False).first()
                if cart:
                    for item in cart.cart_items.all():
                        OrderItem.objects.create(
                            order=order,
                            product=item.product,
                            quantity=item.quantity
                        )
                    # Mark the cart as paid
                    cart.is_paid = True
                    cart.save()
                
                messages.success(request, "Order placed successfully!")
                return redirect('cart')  # Redirect to the cart or success page
            
        else:
            # Form validation failed
            messages.error(request, "There were errors with your submission.")
            return redirect('cart')  # Redirect back to cart if error

    # If the request is not POST, redirect to the cart
    return redirect('cart')
