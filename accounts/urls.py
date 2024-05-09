
from django.urls import path
from accounts.views import login_page, logout_user,register_page, activate_email, add_to_cart, cart, remove_cart, remove_coupon, user_profile
from products import views
from accounts.views import checkout

urlpatterns = [
  path('login/', login_page, name="login"),
  path('register/', register_page, name="register"),
  path('activate/<email_token>/', activate_email, name="activate_email"),
  path('cart/', cart, name="cart"),
  path('add-to-cart/<slug:slug>/', add_to_cart, name="add_to_cart"),
  path('remove-cart/<uuid:cart_item_uid>/', remove_cart, name="remove_cart"),
  path('remove_coupon/<cart_id>/', remove_coupon, name ="remove_coupon"),
  path('checkout/', checkout, name='checkout'),
  path('profile/', user_profile, name='user_profile'),
  path('logout/', logout_user, name='logout_user'),
]
