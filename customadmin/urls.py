from django.shortcuts import redirect
from django.urls import path
from customadmin.views import admin_login, admin_dashboard, admin_logout, delete_coupon, delete_order, delete_product, seller_dashboard, seller_login, seller_logout,  seller_registration, update_order_status 
from customadmin.views import admin_dashboard
# update_product, add_product_image

urlpatterns = [
    path('admin/', lambda request: redirect('admin_login')),  # The default path, which could also be the login page
    path('admin/login/', admin_login, name='admin_login'),  # Admin login path
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/logout/', admin_logout, name='admin_logout'),
    path('delete-product/<str:product_name>/', delete_product, name='delete_product'),  # Route for deleting product by name
    path('update-order-status/<int:order_id>/', update_order_status, name='update_order_status'),
    path('delete-order/<int:order_id>/',delete_order, name='delete_order'),  # URL for order deletion
    # path('coupon-management/', coupon_management, name='coupon_management'),  # Manage coupons
    # Ensure coupon_id is passed to the URL
    path('admin/delete-coupon/<str:coupon_code>/', delete_coupon, name='delete_coupon'),
    # path('add/', add_product, name='add_product'),
    # path('products/update/<int:product_id>/', update_product, name='update_product'),  # Update product
    # path('products/add-image/', add_product_image, name='add_product_image'),
    #  path('user-list/', user_list, name='user_list'),
    path('seller/register/', seller_registration, name='seller_registration'),
    path('seller/login/', seller_login, name='seller_login'),
    path('seller/',seller_dashboard, name='seller_dashboard'),
    path('seller/logout/', seller_logout, name='seller_logout'),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)