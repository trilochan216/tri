from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render



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



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from customadmin.forms import ProductForm, ProductImageFormSet
from products.models import Product, ColorVariant, SizeVariant, ProductImage

@login_required
def admin_dashboard(request):
    products = Product.objects.all()
    users = User.objects.exclude(username='admin')
    
    form = ProductForm()  # Default product form
    formset = ProductImageFormSet(queryset=ProductImage.objects.none())  # Empty formset

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        formset = ProductImageFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            product = form.save()  # Save the product

            # Handle formset submissions for product images
            for form in formset:
                image = form.save(commit=False)
                image.product = product
                image.save()

            return redirect('admin_dashboard')  # Redirect after successful addition

    context = {
        'products': products,
        'users': users,
        'form': form,
        'formset': formset,
    }

    return render(request, 'customadmin/dashboard.html', context)



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