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



@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "order_detail.html", {"order": order})

 

from django import forms
from django.core.mail import EmailMessage
from django.conf import settings
from base.helpers import save_pdf

class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    address = forms.CharField(widget=forms.Textarea)
    payment_method = forms.ChoiceField(
        choices=[("Cash on Delivery", "Cash on Delivery")],  # Ensure this exists
        required=True  # Ensure the field is required
    )

from django.db import transaction
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from .models import Order, OrderItem, Cart
from .forms import CheckoutForm
from .utils import send_order_email  # Functions for PDF generation and sending email

@login_required
def checkout(request):
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():  # Ensure database consistency
                try:
                    # Create the order
                    order = Order.objects.create(
                        user=request.user,
                        name=form.cleaned_data["name"],
                        email=form.cleaned_data["email"],
                        address=form.cleaned_data["address"],
                        payment_method="Cash on Delivery",
                    )
                    
                                    # Fetch cart and cart items
                    cart = Cart.objects.filter(user=request.user, is_paid=False).first()
                    cart_items = cart.cart_items.all() if cart else []
                    cart_total = cart.get_cart_total() if cart else 0
                    if cart:
                        for item in cart.cart_items.all():
                            OrderItem.objects.create(
                                order=order,
                                product=item.product,
                                quantity=item.quantity,
                            )

                        # Mark the cart as paid
                        cart.is_paid = True
                        cart.save()

                    # Generate the PDF for the order
                    pdf_file_name, pdf_success = save_pdf({"order": order, "cart_items": cart.cart_items.all()})
                    if pdf_success:
                        # Construct the full path for the PDF
                        pdf_path = f"{settings.BASE_DIR}/templates/base/{pdf_file_name}.pdf"
                        # Send the order confirmation email with the PDF attachment
                        send_order_email(order, pdf_path)
                    else:
                        messages.error(request, "Failed to generate order PDF.")

                    messages.success(request, "Order placed successfully!")
                    return redirect("cart")  # Redirect to success page
                    
                except Exception as e:
                    messages.error(request, f"An error occurred while placing your order: {str(e)}")
                    return redirect("cart")
            
        else:
            messages.error(request, "Error placing the order. Please check your input.")
            return redirect("cart")  # Redirect back to cart if validation fails

    return redirect("cart")  # Redirect to cart if method is not POST



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import UserEditForm, ProfileEditForm

@login_required
def user_profile(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')  # Get all orders for the logged-in user
    user = request.user
    profile = Profile.objects.get(user=user)
    print(f"User first name: {user.first_name}")  # Check if these are correct
    print(f"User last name: {user.last_name}")

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            print(f"User's first name after saving: {user.first_name}")
            print(f"User's last name after saving: {user.last_name}")
            return redirect(request.path)  # Redirect to the same page after update
        


        messages.error(request, "Failed to update profile. Please check your inputs.")
    
    else:
        user_form = UserEditForm(instance=user)
        profile_form = ProfileEditForm(instance=profile)

    context = {
        'orders': orders,
        'user': user,
        'profile': profile,
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'accounts/Profile.html', context)

from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def logout_user(request):
    logout(request)  # Ends the user's session
    messages.success(request, "You have been logged out successfully.")
    return redirect('index')  # Redirect to the homepage or any other desired page




@login_required
def cancel_order(request, order_id):
    order = Order.objects.get(pk=order_id, user=request.user)  # Get the order for the logged-in user

    if order.can_cancel():
        order.status = OrderStatus.CANCELED  # Update the order status to "Canceled"
        order.save()
        messages.success(request, "Your order has been canceled.")
    else:
        messages.error(request, "Order cancellation is allowed only within 2 hours of order creation.")

    return redirect('user_profile')  # Redirect back to the orders page
