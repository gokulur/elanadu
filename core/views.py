from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login, logout
from .models import OTP,Cart,Order
from shop.models import Product 
CustomUser = get_user_model()
import random
import requests
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.core.mail import send_mail

def registration_page(request):
    return render (request,'registration.html')

def user_update_page(request):
    return render (request,'user_update.html')

def login_page(request):
    return render (request,'login.html')

def user_verification(request):
    return render (request,'verification.html')
 

def user_forgot_page(request):
    return render (request,'forgot.html')

def verify_reset_page(request):
    return render (request,'verifyreset.html')

def change_password_page(request):
    return render (request,'changepassword.html')

def user_cart_page(request):
    return render (request,'usercart.html')




def send_verification_email(to_email, otp):
    subject = "Elanadu Email Verification Code"
    message = f"Your OTP code is: {otp}\nThis code is valid for 10 minutes."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [to_email]

    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        print("Email sent to", to_email)
        return True
    except Exception as e:
        print("Error sending email:", e)
        return False

def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

 
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('registration_page')

        if CustomUser.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already exists.")
            return redirect('registration_page')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('registration_page')

      
        otp = str(random.randint(100000, 999999))

     
        request.session['reg_data'] = {
            'username': username,
            'phone': phone,
            'email': email,
            'password': password,
            'otp': otp
        }

    
        OTP.objects.create(
            code=otp,
            purpose='register',
            user=None,
            expires_at=timezone.now() + timedelta(minutes=10),
            is_used=False
        )

       
        if not send_verification_email(email, otp):
            messages.error(request, "Failed to send verification email.")
            return redirect('registration_page')

        return redirect('user_verification')   

    return redirect('user_verification')

 

def verify_email(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        reg_data = request.session.get('reg_data')

        if not reg_data:
            messages.error(request, "Session expired or invalid.")
            return redirect('registration_page')

        try:
            otp_entry = OTP.objects.get(
                code=entered_otp,
                purpose='register',
                is_used=False,
                expires_at__gt=timezone.now()
            )
        except OTP.DoesNotExist:
            messages.error(request, "Invalid or expired OTP.")
            return redirect('verify_email')

     
        user = CustomUser.objects.create_user(
            username=reg_data['username'],
            phone=reg_data['phone'],
            password=reg_data['password'],
            email=reg_data['email']
        )
 
        otp_entry.is_used = True
        otp_entry.user = user
        otp_entry.save()

    
        del request.session['reg_data']

        messages.success(request, "Registration successful. You can now log in.")
        return redirect('login_page')

    return redirect('login_page')


@login_required
def update_profile(request):
    user = request.user

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        profile_image = request.FILES.get('profile_image')

 
        # if User.objects.exclude(id=user.id).filter(username=username).exists():
        #     messages.error(request, "Username already taken.")
        #     return redirect('update_profile')

        if CustomUser.objects.exclude(id=user.id).filter(phone=phone).exists():
            messages.error(request, "Phone number already taken.")
            return redirect('update_profile')

        user.username = username
        user.email = email
        user.phone = phone
        if profile_image:
            user.profile_image = profile_image
        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('update_profile')

    return render(request, 'users/update_profile.html', {'user': user})




@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect('home')  

    return render(request, 'users/delete_account.html')


def user_login(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        try:
            user_obj = CustomUser.objects.get(phone=phone)
        except CustomUser.DoesNotExist:
            messages.error(request, "Invalid phone number or password.")
            return redirect('login_page')

        user = authenticate(request, username=user_obj.username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect('ProductsView')   
        else:
            messages.error(request, "Invalid phone number or password.")
            return redirect('login_page')

    return redirect('login_page')

def forgot_password_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, "Email not found.")
            return redirect('forgot_password')

        otp = str(random.randint(100000, 999999))

        request.session['reset_email'] = email
        request.session['reset_otp'] = otp

        OTP.objects.create(
            code=otp,
            purpose='reset',
            user=user,
            expires_at=timezone.now() + timedelta(minutes=10),
            is_used=False
        )

        send_verification_email(email, otp)
        messages.success(request, "OTP sent to your email.")
        return redirect('verify_reset_page')

    return redirect('verify_reset_page')

def verify_reset_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        email = request.session.get('reset_email')

        if not email:
            messages.error(request, "Session expired.")
            return redirect('forgot_password')

        try:
            otp_entry = OTP.objects.get(
                code=entered_otp,
                purpose='reset',
                is_used=False,
                expires_at__gt=timezone.now(),
                user__email=email
            )
        except OTP.DoesNotExist:
            messages.error(request, "Invalid or expired OTP.")
            return redirect('verify_reset_page')

        otp_entry.is_used = True
        otp_entry.save()
        messages.success(request, "OTP verified. Set your new password.")
        return redirect('change_password_page')

    return redirect('change_password_page')


def reset_password_form(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.session.get('reset_email')

        if not email:
            messages.error(request, "Session expired.")
            return redirect('forgot_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('reset_password_form')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('forgot_password')

        user.set_password(password)
        user.save()

     
        del request.session['reset_email']
        del request.session['reset_otp']

        messages.success(request, "Password reset successful. Please login.")
        return redirect('login_page')

    return redirect('login_page')



@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login_page')


@login_required
def user_profile(request):
    user = request.user
    return render(request, 'users/profile.html', {'user': user})

 
@login_required
def user_cart(request):
    user = request.user
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        Cart.objects.create(product=product, user=user)
        messages.success(request, "Product added to cart.")
        return redirect('user_cart')

@login_required
def user_order(request):
    user = request.user
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        total_amount = product.price
        Order.objects.create(product=product, user=user, total_amount=total_amount)
        messages.success(request, "Order placed successfully.")
        return redirect('user_order')                            