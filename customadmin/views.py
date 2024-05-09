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


# @login_required
# def admin_dashboard(request):
#     form = ProductForm()  # Main product form
#     color_formset = ColorVariantFormSet(queryset=ColorVariant.objects.none())  # Initialize with no data
#     size_formset = SizeVariantFormSet(queryset=SizeVariant.objects.none())  # Initialize with no data
#     image_formset = ProductImageFormSet(queryset=ProductImage.objects.none())  # Initialize with no data

#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)  # Include FILES for file uploads
#         color_formset = ColorVariantFormSet(request.POST, request.FILES)  # Reinitialize with POST data
#         size_formset = SizeVariantFormSet(request.POST, request.FILES)  # Reinitialize with POST data
#         image_formset = ProductImageFormSet(request.POST, request.FILES)  # Reinitialize with POST data

#         if form.is_valid() and image_formset.is_valid():  # Ensure required forms are valid
#             product = form.save(commit=False)  # Save without committing
#             product.save()  # Save the product to the database

#             # Optional handling for color variants
#             if color_formset.is_valid():  # Ensure formset is valid
#                 for color_form in color_formset:
#                     if color_form.cleaned_data:  # Ensure there's valid data
#                         color_instance = color_form.save(commit=False)
#                         color_instance.save()  # Save the color variant
#                         product.color_variant.add(color_instance)  # Associate with the product

#             # Optional handling for size variants
#             if size_formset.is_valid():
#                 for size_form in size_formset:
#                     if size_form.cleaned_data:  # Ensure there's valid data
#                         size_instance = size_form.save(commit=False)
#                         size_instance.save()  # Save the size variant
#                         product.size_variant.add(size_instance)  # Associate with the product

#             # Required handling for product images
#             if image_formset.is_valid():
#                 for image_form in image_formset:
#                     if image_form.cleaned_data:
#                         image_instance = image_form.save(commit=False)
#                         image_instance.product = product  # Associate with the product
#                         image_instance.save()  # Save the image

#             return redirect('admin_dashboard')  # Redirect after successful save

#     # Context to pass to the template
#     context = {
#         'products': Product.objects.all(),  # All products
#         'users': User.objects.exclude(username='admin'),  # All non-admin users
#         'form': form,  # Product form
#         'color_formset': color_formset,  # Formset for color variants
#         'size_formset': size_formset,  # Formset for size variants
#         'image_formset': image_formset,  # Formset for product images
#     }

#     return render(request, 'customadmin/dashboard.html', context)  # Render the dashboard template






from django.shortcuts import render, redirect
from accounts.models import Order, OrderItem, OrderStatus
from customadmin.forms import ProductForm, ColorVariantFormSet, SizeVariantFormSet, ProductImageFormSet
from products.models import Product
from django.contrib.auth.models import User

def admin_dashboard(request):
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







# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from products.models import Product, ColorVariant, SizeVariant, ProductImage
# from customadmin.forms import ProductForm, ColorVariantForm, SizeVariantForm, ProductImageForm





# @login_required
# def add_product(request):
#     if request.method == 'POST':
#         product_form = ProductForm(request.POST, request.FILES)  # Form handling for POST
#         if product_form.is_valid():
#             product_form.save()  # Save the product
#             return redirect('admin_dashboard')  # Redirect after saving
#     else:
#         product_form = ProductForm()  # Form initialization for GET
    
#     context = {
#         'product_form': product_form,  # Pass the form to the template
#     }
    
#     return render(request, 'customadmin/dashboard.html', context)  # Ensure the correct template is rendered











# @login_required
# def update_product(request, product_id):
#     product = get_object_or_404(Product, id=product_id)  # Get the product by ID
#     if request.method == 'POST':
#         product_form = ProductForm(request.POST, request.FILES, instance=product)  # Handle form submission
#         if product_form.is_valid():
#             product_form.save()  # Save the updated product
#             return redirect('admin_dashboard')  # Redirect after successful update
#     else:
#         product_form = ProductForm(instance=product)  # Prefill form with existing data
    
#     context = {
#         'product_form': product_form,
#     }
    
#     return render(request, 'customadmin/dashboard.html', context)  # Render the form



# @login_required
# def add_product_image(request, product_id):
#     product = get_object_or_404(Product, id=product_id)  # Get the product by ID
#     if request.method == 'POST':
#         image_form = ProductImageForm(request.POST, request.FILES)  # Handle image uploads
#         if image_form.is_valid():
#             # Create and associate the new image with the product
#             product_image = image_form.save(commit=False)
#             product_image.product = product  # Associate with the product
#             product_image.save()  # Save the new product image
            
#             return redirect('update_product', product_id=product_id)  # Redirect back to update_product
#     else:
#         image_form = ProductImageForm()  # Initial GET request
    
#     context = {
#         'product': product,
#         'image_form': image_form,
#     }
    
#     return render(request, 'customadmin/dashboard.html', context)  # Render the form