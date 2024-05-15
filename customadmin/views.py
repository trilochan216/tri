from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.models import Order, OrderItem, OrderStatus
from products.models import ColorVariant, Product, ProductImage, SizeVariant



def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')  # Redirects to dashboard for authenticated users
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)  # Authenticate user
        
        if user and user.is_superuser:
            login(request, user)  # Log in the user
            return redirect('admin_dashboard')  # Redirects to dashboard
        else:
            messages.error(request, "Invalid username or password")
            return HttpResponseRedirect(request.path_info)  # Reloads login page
    
    return render(request, 'customadmin/admin_login.html')  # Returns login template



@login_required  # Make sure this decorator is applied to require login
def admin_dashboard(request):
    return render(request, 'customadmin/dashboard.html') 


from django.shortcuts import redirect
from django.contrib.auth import logout

def admin_logout(request):
    logout(request)  # Logs out the user
    return redirect('admin_login')  # Redirects to the login page after logout


from customadmin.forms import ProductForm, ColorVariantFormSet, SizeVariantFormSet, ProductImageFormSet




from django.shortcuts import render, redirect
from customadmin.forms import ProductForm, ColorVariantFormSet, SizeVariantFormSet, ProductImageFormSet
from products.models import Product, ColorVariant, SizeVariant, ProductImage
from django.contrib.auth.decorators import login_required




from django.shortcuts import render, redirect
from accounts.models import Order, OrderItem, OrderStatus
from customadmin.forms import ProductForm, ColorVariantFormSet, SizeVariantFormSet, ProductImageFormSet
from products.models import Product
from django.contrib.auth.models import User

def admin_dashboard(request):
    
    
    sellers = Seller.objects.all()

    if request.method == 'POST':
        # Check if the request is for verifying a seller
        if 'verify_seller' in request.POST:
            seller_id = request.POST.get('seller_id')
            seller = Seller.objects.get(pk=seller_id)
            seller.is_verified = True
            seller.save()
            # Redirect to avoid resubmission
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
    # Fetch all orders
    orders = Order.objects.all()
    
    # Build a dictionary of order items by order ID
    order_items_by_order = {order.id: order.items.all() for order in orders}

    # Calculate total amount for each order
    total_amount_by_order = {
        order.id: order.total_price()  # Corrected with parentheses
        for order in orders
    }
    
    
        # Calculate total sales for completed orders
    total_sales = sum(
        order.total_price() for order in orders if order.status == OrderStatus.COMPLETED
    )
    
    total_orders = orders.count()
    
    total_products = Product.objects.count()
    
    
    coupons = Coupon.objects.all()
    coupon_form = CouponForm()
    existing_coupons = Coupon.objects.all()  # Fetch existing coupons
    
    if request.method == 'POST':
        coupon_form = CouponForm(request.POST)  # Process coupon form
        
        if coupon_form.is_valid():
            coupon_form.save()  # Save the new coupon
            messages.success(request, 'Coupon added successfully!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))   # Redirect to avoid resubmission

    # Product form and formsets for colors, sizes, and images
    form = ProductForm()
    color_formset = ColorVariantFormSet(queryset=ColorVariant.objects.none())
    size_formset = SizeVariantFormSet(queryset=SizeVariant.objects.none())
    image_formset = ProductImageFormSet(queryset=ProductImage.objects.none())

    # Handling POST request for new product submissions
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        color_formset = ColorVariantFormSet(request.POST, request.FILES)
        size_formset = SizeVariantFormSet(request.POST, request.FILES)
        image_formset = ProductImageFormSet(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.save()

            # Add color variants if formset is valid
            if color_formset.is_valid():
                for color_form in color_formset:
                    if color_form.cleaned_data:
                        color_instance = color_form.save(commit=False)
                        color_instance.save()
                        product.color_variant.add(color_instance)

            # Add size variants if formset is valid
            if size_formset.is_valid():
                for size_form in size_formset:
                    if size_form.cleaned_data:
                        size_instance = size_form.save(commit=False)
                        size_instance.save()
                        product.size_variant.add(size_instance)

            # Add product images
            if image_formset.is_valid():
                for image_form in image_formset:
                    if image_form.cleaned_data:
                        image_instance = image_form.save(commit=False)
                        image_instance.product = product
                        image_instance.save()

            return redirect('admin_dashboard')

    # Prepare the context for rendering
    context = {
        'coupons': coupons,
        'coupon_form': coupon_form,
        'existing_coupons': existing_coupons,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_sales': total_sales,
        'orders': orders,
        'order_items_by_order': order_items_by_order,
        'total_amount_by_order': total_amount_by_order,
        'order_status_choices': [choice[0] for choice in OrderStatus.choices],
        'products': Product.objects.all(),
        'users': User.objects.exclude(username='admin'),
        'form': form,
        'color_formset': color_formset,
        'size_formset': size_formset,
        'image_formset': image_formset,
        'sellers': sellers,
    }

    return render(request, 'customadmin/dashboard.html', context)



from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from products.models import Product
from django.contrib import messages

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from products.models import Product

@login_required
def delete_product(request, product_name):
    # Get the product by name (ensure case-insensitive to avoid errors)
    product = get_object_or_404(Product, product_name=product_name)
    

    # Handle only POST requests to delete the product
    if request.method == 'POST':
        product.delete()  # Delete the product
        messages.success(request, f"Product '{product.product_name}' has been deleted successfully.")

        # Redirect back to the same page or a specified URL
        previous_url = request.META.get('HTTP_REFERER', '/')
        return HttpResponseRedirect(previous_url)  # Redirect back to the referring page

    return redirect('admin_dashboard')  # Fallback if not a POST request





from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from accounts.models import Order

def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')  # Get the new status from the POST data
        if new_status:
            order.status = new_status  # Update the order status
            order.save()  # Save the changes
            messages.success(request, f"Order status updated to '{new_status}'.")
        else:
            messages.error(request, "Invalid status.")  # Handle empty status

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # Redirect back to the dashboard










from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import Order

@login_required
def delete_order(request, order_id):
    # Check if the order exists and delete it
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    messages.success(request, f"Order #{order_id} deleted successfully.")
    return redirect('admin_dashboard')  # Redirect back to the dashboard








# customadmin/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from customadmin.forms import CouponForm
from products.models import Coupon
from django.shortcuts import get_object_or_404

from django.shortcuts import redirect
from django.contrib import messages
from products.models import Coupon

def delete_coupon(request, coupon_code):
    try:
        coupon = Coupon.objects.get(coupon_code=coupon_code)  # Find the coupon by code
        coupon.delete()  # Delete the coupon
        messages.success(request, f'Coupon "{coupon_code}" deleted successfully.')
    except Coupon.DoesNotExist:
        messages.error(request, f'Coupon "{coupon_code}" not found.')
    return redirect('admin_dashboard')  # Redirect back to dashboard




# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SellerRegistrationForm

def seller_registration(request):
    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now login.')
            return redirect('seller_login')  # Assuming 'seller_login' is the name of your login URL
        else:
            messages.error(request, 'Form submission failed. Please correct errors.')
    else:
        form = SellerRegistrationForm()
    return render(request, 'customadmin/seller_registration.html', {'form': form})



from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from .forms import SellerLoginForm
from .models import Seller

def seller_login(request):
    if request.method == 'POST':
        form = SellerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                seller = Seller.objects.get(email=email)
                if check_password(password, seller.password):
                    if seller.is_verified:
                        # Authentication successful
                        # Set session variables or login user if needed
                        messages.success(request, 'Login successful.')
                        return redirect('seller_dashboard')
                    else:
                        # Seller is not verified
                        messages.error(request, 'Your account is not verified yet.')
                else:
                    messages.error(request, 'Invalid email or password.')
            except Seller.DoesNotExist:
                messages.error(request, 'Invalid email or password.')
    else:
        form = SellerLoginForm()
    return render(request, 'customadmin/seller_login.html', {'form': form})



# views.py
# views.py

# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CouponForm
from products.models import Coupon

@login_required(login_url='seller_login')
def seller_dashboard(request):
    # Fetch products, orders, and coupons
    products = Product.objects.all()
    orders = Order.objects.all()
    coupons = Coupon.objects.all()
    coupon_form = CouponForm()  # Add coupon form instance
    
    if request.method == 'POST':
        coupon_form = CouponForm(request.POST)
        if coupon_form.is_valid():
            coupon_form.save()
            messages.success(request, 'Coupon added successfully.')
            return redirect('seller_dashboard')
        else:
            messages.error(request, 'Invalid coupon data.')
    
    return render(request, 'customadmin/seller_dashboard.html', {'products': products, 'orders': orders, 'coupons': coupons, 'coupon_form': coupon_form})




from django.contrib.auth import logout
from django.shortcuts import redirect

def seller_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('seller_login')
    else:
        # Handle GET requests, if needed
        pass
