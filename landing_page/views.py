from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout
from django.conf import settings
from django.http import HttpResponseRedirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
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
        country_code = '+44'
        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            country_code = profile.country_code
        YOUR_DOMAIN = "https://yogshalaa.in/"
        # if request.method == 'POST':
        if 'Weekend flow' in request.POST:  # For Weekend Flow
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price': ('price_1NDlGVSFpSBjt2aIQHiDadJP' if country_code == '+44'
                                  else 'price_1NKIbOSFpSBjt2aIjJK9DxBb'),
                        # Can be created on Stripe Dashboard
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
                        'price': ('price_1NDlHhSFpSBjt2aIHFT5Me9E' if country_code == '+44'
                                  else 'price_1NKIX5SFpSBjt2aIdz69Guxc'),
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
                        'price': ('price_1NDlHoSFpSBjt2aITL7JDNje' if country_code == '+44'
                                  else 'price_1NKIRvSFpSBjt2aIW59sbRqS'),
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
                        'price': ('price_1NDlHxSFpSBjt2aIFIxQjhmj' if country_code == '+44'
                                  else 'price_1NKIYQSFpSBjt2aIj5dXRFUp'),
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
        try:
            priceDict = {'priceRegularMonthly': 0, 'priceRegularQuarterly': 0,
                         'pricePersonalizedSessions': 0, 'priceWeekendFlow': 0}
            currency = '£'
            discount = '18.8%'
            if request.user.is_authenticated:
                profile = Profile.objects.get(user=request.user)
                if profile.country_code == '+91':
                    priceDict['priceRegularMonthly'] = 1500
                    priceDict['priceRegularQuarterly'] = 4000
                    priceDict['pricePersonalizedSessions'] = 500
                    priceDict['priceWeekendFlow'] = 500
                    currency = '₹'
                    discount = '11.11%'
                else:
                    priceDict['priceRegularMonthly'] = 99
                    priceDict['priceRegularQuarterly'] = 249
                    priceDict['pricePersonalizedSessions'] = 14.99
                    priceDict['priceWeekendFlow'] = 13.99
            return render(request, 'success.html', {'priceRegularMonthly': priceDict['priceRegularMonthly'],
                                                    'priceRegularQuarterly': priceDict['priceRegularQuarterly'],
                                                    'pricePersonalizedSessions': priceDict['pricePersonalizedSessions'],
                                                    'priceWeekendFlow': priceDict['priceWeekendFlow'],
                                                    'currencySymbol': currency,
                                                    'discount': discount
                                                    })
        except Exception as e:
            print(e)
            logout(request)
            return render(request, 'register.html', {})
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
        print(phone_num)
        if Profile.objects.filter(mobile=phone_num).exists():
            red = redirect('User Landing Page')
            red.set_cookie('profile_verified', True, max_age=86400)
            return red

        user = User.objects.create(
            username=f'Yogshalaa_user_{request.POST["full_name"]}_{uuid.uuid4().hex[:6].upper()}')
        otp = random.randint(1000, 9999)
        profile = Profile.objects.create(user=user, mobile=phone_num, otp=f'{otp}', country_code=country_code)
        messageHandler = OTPHandler(phone_num, otp).send_otp_via_message()
        print(messageHandler)
        red = redirect(f'otp/{profile.uid}/')
        red.set_cookie("can_otp_enter", True, max_age=600)
        return red
    return render(request, 'register.html')


def verifyOTP(request, uid):
    # uid = Profile.uid
    if request.method == "POST":
        try:
            profile = Profile.objects.get(uid=uid)
        except Exception as e:
            messages.info(request, f"{e}: The given profile doesn't exist. Please register.")
            return render(request, "register.html", {'data': 'something'})
        try:
            resend_code = request.POST.get('resend_code', False)
        except Exception as e:
            messages.info(request, f"Please wait for sometime.")
            return render(request, f'otp/{profile.uid}')
        if resend_code:
            otp = random.randint(1000, 9999)
            messageHandler = OTPHandler(profile.mobile, otp).send_otp_via_message()
            print(messageHandler)
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
            try:
                profile = Profile.objects.get(mobile=f'+{country_code}{phone_number}')
            except Exception as e:
                messages.info(request, 'Phone number entered is incorrect')
                return render(request, 'login.html', {'data': 'something'})
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
    red = redirect('login')
    red.delete_cookie('profile_verified')
    return red


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
