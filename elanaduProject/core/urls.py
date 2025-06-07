from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.user_register, name='user_register'),
    path('registration/', views.registration_page, name='registration_page'),
    path('user_update_page/', views.user_update_page, name='user_update_page'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('login/', views.user_login, name='user_login'),
    path('login_page/', views.login_page, name='login_page'),
    path('logout/', views.user_logout, name='user_logout'),
    path('verify/', views.user_verification, name='user_verification'),
    path('verify_email/', views.verify_email, name='verify_email'),
    path('user_forgot/', views.user_forgot_page, name='userforgotpage'),
    path('forgot_password_request/', views.forgot_password_request, name='forgot_password_request'),
    path('verify_reset_page/', views.verify_reset_page, name='verify_reset_page'),
    path('verify_reset_otp/', views.verify_reset_otp, name='verify_reset_otp'),
    path('change_password_page/', views.change_password_page, name='change_password_page'),
    path('reset_password_form/', views.reset_password_form, name='reset_password_form'),
    # path('reset_password_form/', views.reset_password_form, name='reset_password_form'),

    path('user_cart_page/', views.user_cart_page, name='user_cart_page'),
    path('user_cart/', views.user_cart, name='user_cart'),
    path('user_order/', views.user_order, name='user_order'),
    # path('user_order_page/', views.user_order_page, name='user_order_page'),
    path('order/', views.order_page, name='order_page'),
    path('profile/', views.user_profile_page, name='user_profile'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('user_cart_order/', views.user_cart_order, name='user_cart_order'),
]