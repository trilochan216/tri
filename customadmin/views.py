from django.shortcuts import render, redirect
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
