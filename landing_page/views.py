from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout
from django.conf import settings
from django.http import HttpResponseRedirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Profile
from .helpers import OTPHandler
import stripe
import random
import uuid

# Create your views here.

# Stripe product config
stripe.api_key = settings.SECRET_KEY_PROD


# Checkout session for accepting payments
def create_checkout_session(request):
    checkout_session = None
    try:
        YOUR_DOMAIN = "https://yogshalaa.in/"
        # if request.method == 'POST':
        if 'Weekend flow' in request.POST:  # For Weekend Flow
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price': 'price_1NDlGVSFpSBjt2aIQHiDadJP',  # Can be created on Stripe Dashboard
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                success_url=YOUR_DOMAIN + 'success',
                cancel_url=YOUR_DOMAIN + 'cancel',
            )
        elif 'Personalized flow' in request.POST:  # For personalized sessions
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': 'price_1NDlHhSFpSBjt2aIHFT5Me9E',
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + 'success',
                cancel_url=YOUR_DOMAIN + 'cancel',
            )

        elif 'Morning flow Monthly' in request.POST:  # For Monthly Morning Energized Flow
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': 'price_1NDlHoSFpSBjt2aITL7JDNje',
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + 'success',
                cancel_url=YOUR_DOMAIN + 'cancel',
            )

        elif 'Morning flow Quarterly' in request.POST:  # For Quarterly Morning Energized Flow
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': 'price_1NDlHxSFpSBjt2aIFIxQjhmj',
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + 'success',
                cancel_url=YOUR_DOMAIN + 'cancel',
            )
        return redirect(checkout_session.url, code=303)

    except Exception as e:
        print("Exception occurred: " + str(e))
        return str(e)


# User Dashboard
def success_page(request):
    if request.COOKIES.get('profile_verified') is not None:
        return render(request, 'success.html', {'data': 'Something'})
    else:
        logout(request)
        red = redirect('login')
        red.delete_cookie('profile_verified')
        return red


def registerView(request):
    if request.COOKIES.get('profile_verified') is not None:
        return redirect('User Landing Page')
    if request.method == 'POST':
        phone_num = request.POST['phone_number']
        country_code = f"+{request.POST['country_code']}"
        phone_num = f'{country_code}{phone_num}'
        if Profile.objects.filter(mobile=phone_num).exists():
            red = redirect('User Landing Page')
            red.set_cookie('profile_verified', True, max_age=86400)
            return red

        user = User.objects.create(
            username=f'Yogshalaa_user_{request.POST["full_name"]}_{uuid.uuid4().hex[:6].upper()}')
        otp = random.randint(1000, 9999)
        profile = Profile.objects.create(user=user, mobile=phone_num, otp=f'{otp}', country_code=country_code)
        OTPHandler(phone_num, otp, country_code).send_otp_via_message()
        red = redirect(f'otp/{profile.uid}/')
        red.set_cookie("can_otp_enter", True, max_age=600)
        return red
    return render(request, 'register.html')


def verifyOTP(request, uid):
    # uid = Profile.uid
    if request.method == "POST":
        profile = Profile.objects.get(uid=uid)
        resend_code = request.POST.get('resend_code', False)
        if resend_code:
            otp = random.randint(1000, 9999)
            OTPHandler(profile.mobile, otp, profile.country_code).send_otp_via_message()
            profile.otp = otp
            profile.save()
            red = HttpResponseRedirect(request.path_info)
            red.set_cookie("can_otp_enter", True, max_age=600)
            return red
        elif request.COOKIES.get('can_otp_enter') is not None:
            if profile.otp == request.POST['otp']:
                user = profile.user
                login(request, user)
                red = redirect("User Landing Page")
                red.set_cookie('profile_verified', True, max_age=86400)
                return red
            return HttpResponse("wrong otp")
        return HttpResponse("10 minutes passed")
    return render(request, "verifyOTP.html", {'uid': uid})


def loginView(request):

    if request.user.is_authenticated:
        red = redirect('User Landing Page')
        red.set_cookie('profile_verified', True, max_age=86400)
        return red

    else:
        if request.method == 'POST':
            phone_number = request.POST.get('phone_number')
            country_code = request.POST.get('country_code')
            profile = Profile.objects.get(mobile=f'+{country_code}{phone_number}')
            user = profile.user

            if Profile.objects.filter(mobile=f'+{country_code}{phone_number}').exists():
                print("User already exists", f'+{country_code}{phone_number}')
                login(request, user)
                red = redirect('User Landing Page')
                red.set_cookie('profile_verified', True, max_age=86400)
                return red
            else:
                messages.info(request, 'Phone number entered is incorrect')
                return render(request, 'login.html', {'data': 'something'})

    context = {}
    return render(request, "login.html", context)


def logoutView(request):
    logout(request)
    return redirect('login')


def coverageView(request):
    return render(request, 'classCoverage.html', {'data': 'something'})


def photoGallery(request):
    return render(request, 'Gallery.html', {'data': 'something'})


def cancelCheckoutSession(request):
    return render(request, 'cancel.html', {'data': 'something'})


def signUpView(request):
    red = redirect('register')
    red.delete_cookie('profile_verified')
    return red


def trialClassView(request):
    return render(request, 'trial_new.html', {'data': 'something'})
