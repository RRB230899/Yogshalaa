from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views import View
from .models import YogaUser, Profile
from .helpers import OTPHandler
import requests
import stripe
import random
import http.client
import uuid

# Create your views here.

# Stripe product config
stripe.api_key = settings.SECRET_KEY_PROD


def create_checkout_session(request):
    try:
        YOUR_DOMAIN = "https://yogshalaa.in/"
        # if request.method == 'POST':
        if 'Weekend flow' in request.POST:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price': 'price_1NDlGVSFpSBjt2aIQHiDadJP',
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                success_url=YOUR_DOMAIN + 'success',
                cancel_url=YOUR_DOMAIN + 'cancel',
            )
        elif 'Personalized flow' in request.POST:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price': 'price_1NDlHhSFpSBjt2aIHFT5Me9E',
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + 'success',
                cancel_url=YOUR_DOMAIN + 'cancel',
            )

        elif 'Morning flow Monthly' in request.POST:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price': 'price_1NDlHoSFpSBjt2aITL7JDNje',
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + 'success',
                cancel_url=YOUR_DOMAIN + 'cancel',
            )

        elif 'Morning flow Quarterly' in request.POST:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
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


@login_required(login_url='/login', redirect_field_name='register')
def success_page(request):
    return render(request, 'success.html', {'data': 'Something'})


def registerView(request):

    if request.method == 'POST':
        phone_num = request.POST['phone_number']
        if Profile.objects.filter(mobile=phone_num).exists():
            return redirect('User Landing Page')
            # return HttpResponse("User already exists.. Please login")

        user = User.objects.create(username=f'Yogshalaa_user_{request.POST["full_name"]}_{uuid.uuid4().hex[:6].upper()}')
        otp = random.randint(1000, 9999)
        profile = Profile.objects.create(user=user, mobile=phone_num, otp=f'{otp}')
        messagehandler = OTPHandler(phone_num, otp, request.POST['country_code']).send_otp_via_message()
        red = redirect(f'otp/{profile.uid}/')
        red.set_cookie("can_otp_enter", True, max_age=600)
        return red
    return render(request, 'register.html')


def sendOTP(request):
    pass


def verifyOTP(request, uid):
    # uid = Profile.uid
    if request.method == "POST":
        profile = Profile.objects.get(uid=uid)
        if request.COOKIES.get('can_otp_enter') is not None:
            if profile.otp == request.POST['otp']:
                red = redirect("User Landing Page")
                red.set_cookie('verified', True)
                return red
            return HttpResponse("wrong otp")
        return HttpResponse("10 minutes passed")
    return render(request, "verifyOTP.html", {'uid': uid})


def loginView(request):

    if request.user.is_authenticated:
        return redirect('User Landing Page')

    else:
        if request.method == 'POST':
            phone_number = request.POST.get('phone_number')
            profile = Profile.objects.get(mobile=phone_number)
            user = profile.user
            # profile = authenticate(request, username=username, password=password)

            if Profile.objects.filter(mobile=phone_number).exists():
                login(request, user)
                return redirect('User Landing Page')
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
