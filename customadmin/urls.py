from django.shortcuts import redirect
from django.urls import path
from customadmin.views import admin_login, admin_dashboard, admin_logout 
from customadmin.views import admin_dashboard
# update_product, add_product_image

urlpatterns = [
    path('admin/', lambda request: redirect('admin_login')),  # The default path, which could also be the login page
    path('admin/login/', admin_login, name='admin_login'),  # Admin login path
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/logout/', admin_logout, name='admin_logout'),
    # path('add/', add_product, name='add_product'),
    # path('products/update/<int:product_id>/', update_product, name='update_product'),  # Update product
    # path('products/add-image/', add_product_image, name='add_product_image'),
    #  path('user-list/', user_list, name='user_list'),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)