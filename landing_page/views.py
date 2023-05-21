from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from .models import UserOTP
from django.views import View
from .models import YogaUser, Profile
import requests
import random
import http.client

# Create your views here.


# @login_required(login_url='login')
def success_page(request):
    return render(request, 'success.html', {'data': 'Something'})


def send_otp(mobile, otp):
    authkey = '397111Ai5h91hdkVp36468d8f5P1'
    conn = http.client.HTTPConnection("api.msg91.com")
    url = "https://control.msg91.com/api/sendotp.php?otp="+otp+'&sender=ABC&message='+otp+'&mobile='+mobile+'&authkey='+\
          authkey+'&country=91'
    # payload = {
    #     "Param1": "value1",
    #     "Param2": "value2",
    #     "Param3": "value3"
    # }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authkey": authkey
    }
    conn.request("GET", url, headers=headers)
    response = conn.getresponse()
    # response = requests.post(url, json=payload, headers=headers)

    print(response)
    return None


def registerView(request):

    if request.user.is_authenticated:
        return redirect('User landing page')
    else:
        form = UserCreationForm()

        if request.method == 'POST':
            # form = UserCreationForm(request.POST)
            # if form.is_valid():
            #     form.save()
            #     user = form.cleaned_data.get('username')
            #     messages.success(request, f"Account successfully created for {user}")
            #     return redirect('login')
            email = request.POST.get('email')
            name = request.POST.get('full_name')
            mobile = request.POST.get('phone_num')

            check_user = User.objects.filter(email=email).first()
            check_profile = Profile.objects.filter(mobile=mobile).first()
            if check_user or check_profile:
                context = {'message': 'User already registered', 'class': 'danger'}
                return render(request, 'register.html', context)

            user = User(email=email, first_name=name)
            user.save()

            otp = str(random.randint(1000, 9999))
            profile = Profile(user=user, mobile=mobile, otp=otp)
            profile.save()
            send_otp(mobile, otp)
            request.session['mobile'] = mobile
            return redirect('login')

    context = {'form': form}
    return render(request, 'register.html', context)


def otp(request):
    mobile = request.session['mobile']


def loginView(request):

    if request.user.is_authenticated:
        return redirect('User landing page')

    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('User landing page')
            else:
                messages.info(request, 'Username or Password is incorrect')
                return render(request, 'login.html', {'data': 'something'})

    context = {}
    return render(request, "login.html", context)


def logoutView(request):
    logout(request)
    return redirect('login')

#
# def userLandingPage(View):
#     userLoginForm = YogaUser.objects.all()


# @api_view(['POST'])
# def sendOTP(request):
#     data = request.data
#
#     if data.get('phone_number') is None:
#         return Response({
#             'status': 400,
#             'message': 'key phone_number is required'
#         })
#
#     if data.get('password') is None:
#         return Response({
#             'status': 400,
#             'message': 'key password is required'
#         })
#
#     user = UserOTP.create(
#         phone_number=data.get('phone_number'),
#         otp=send_otp(data.get('phone_number'))
#     )
#     user.set_password = data.get('set_password')
#     user.save()
#
#     return Response({
#         'status': 200,
#         'message': 'OTP Sent'
#     })
#
#
# @api_view(['POST'])
# def verifyOTP(request):
#     data = request.data
#
#     if data.get('phone_number') is None:
#         return Response({
#             'status': 400,
#             'message': 'key phone_number is required'
#         })
#
#     if data.get('otp') is None:
#         return Response({
#             'status': 400,
#             'message': 'key otp is required'
#         })
#
#     try:
#         user_obj = UserOTP.objects.get(phone_number=data.get('phone_number'))
#
#     except Exception as e:
#         return Response({
#             'status': 400,
#             'message': 'invalid otp'
#         })
#
#     if user_obj.otp == data.get('otp'):
#         user_obj.is_phone_verified = True
#         user_obj.save()
#         return Response({
#             'status': 200,
#             'message': 'OTP matched'
#         })
#     else:
#         return Response({
#             'status': 400,
#             'message': 'invalid otp'
#         })
