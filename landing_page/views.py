from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.conf import settings
from django.http import HttpResponseRedirect
from .models import *
from .helpers import OTPHandler
from django.http import JsonResponse
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
        print('1')
        try:
            print('2')
            priceDict = {'priceRegularMonthly': 0, 'priceRegularQuarterly': 0,
                         'pricePersonalizedSessions': 0, 'priceWeekendFlow': 0}
            currency = '£'
            discount = '18.8%'
            timing1 = ''
            timing2 = ''
            if request.user.is_authenticated:
                print(request.user, 'authenticated')
                profile = Profile.objects.get(user=request.user)
                print(profile)
                if profile.country_code == '+91':
                    print('India')
                    priceDict['priceRegularMonthly'] = 1500
                    priceDict['priceRegularQuarterly'] = 4000
                    priceDict['pricePersonalizedSessions'] = 500
                    priceDict['priceWeekendFlow'] = 500
                    currency = '₹'
                    discount = '11.11%'
                    timing1 = '(6:15-7-15 A.M. (I.S.T.))'
                    timing2 = '(6-7 P.M. (I.S.T.))'
                else:
                    priceDict['priceRegularMonthly'] = 99
                    priceDict['priceRegularQuarterly'] = 249
                    priceDict['pricePersonalizedSessions'] = 14.99
                    priceDict['priceWeekendFlow'] = 13.99
                    timing1 = '(6-7 A.M. (B.S.T.))'
                    timing2 = '(7-8 A.M. (B.S.T.))'
            return render(request, 'success.html', {'priceRegularMonthly': priceDict['priceRegularMonthly'],
                                                    'priceRegularQuarterly': priceDict['priceRegularQuarterly'],
                                                    'pricePersonalizedSessions': priceDict['pricePersonalizedSessions'],
                                                    'priceWeekendFlow': priceDict['priceWeekendFlow'],
                                                    'currencySymbol': currency, 'discount': discount,
                                                    'batchTimings1': timing1, 'batchTimings2': timing2
                                                    })
        except Exception as e:
            print(e, 'Another exception')
            logout(request)
            red = redirect('register')
            red.delete_cookie('profile_verified')
            return red
    else:
        logout(request)
        red = redirect('login')
        red.delete_cookie('profile_verified')
        return red


def registerView(request):
    if request.COOKIES.get('profile_verified') is not None:
        return redirect('User Landing Page')
    if request.method == 'POST':
        try:
            phone_num = request.POST['phone_number']
            country_code = f"+{request.POST['country_code']}"
            phone_num = f'{country_code}{phone_num}'
        except Exception as e:
            print(str(e), 'exception occurred')
            return render(request, 'register.html', {})
        if Profile.objects.filter(mobile=phone_num).exists():
            profile = Profile.objects.get(mobile=phone_num)
            user = User.objects.get(username=profile.user)
            login(request, user)
            red = redirect('User Landing Page')
            red.set_cookie('profile_verified', True, max_age=86400)
            return red

        try:
            user = User.objects.create(
                username=f'Yogshalaa_user_{request.POST["full_name"]}_{uuid.uuid4().hex[:6].upper()}')
            print(user)
            otp = random.randint(1000, 9999)
            profile = Profile.objects.create(user=user, mobile=phone_num, otp=f'{otp}', country_code=country_code)
            messageHandler = OTPHandler(phone_num, otp).send_otp_via_message()
            print(messageHandler)
            red = redirect(f'otp/{profile.uid}/')
            red.set_cookie("can_otp_enter", True, max_age=600)
            return red
        except Exception as e:
            print(str(e))
            return render(request, 'register.html', {})
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
            return render(request, f'otp/{profile.uid}', {'error': str(e)})
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
                red.delete_cookie('can_otp_enter')
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
                return render(request, 'login.html', {'error': str(e)})
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
    try:
        if request.user.is_authenticated:
            return render(request, 'trial_new.html', {'data': 'something'})
        else:
            print('Exception occurred while accessing trial class in try block')
            return redirect('login')
    except Exception as e:
        print('Exception occurred while accessing trial class', str(e))
        return redirect('login')


def my_def_in_view(request):
    data = {}
    if request.method == 'GET':
        try:
            result = dict(request.GET)
            print(result, ': result.achieved')
            # Any process that you want
            # print(json.loads(result))
            user = request.user
            profile = Profile.objects.get(user=user)
            TrialClassUserPreferences.objects.create(profile=profile,
                                                     phone_num=profile.mobile,
                                                     focus_choices=result['focus'],
                                                     style_choices=result['style'])
            data = {
                # Data that you want to send to javascript function
                'result': result
            }
            print(data)
        except Exception as e:
            print('Exception occurred while getting trial class data;', str(e))
            return redirect('Start your free trial')
    return JsonResponse(data)
