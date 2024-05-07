from django.shortcuts import redirect
from django.urls import path
from customadmin.views import admin_login, admin_dashboard, admin_logout

urlpatterns = [
    path('admin/', lambda request: redirect('admin_login')),  # The default path, which could also be the login page
    path('admin/login/', admin_login, name='admin_login'),  # Admin login path
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/logout/', admin_logout, name='admin_logout'),
]


