from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .models import YogaUser
import requests

# Create your views here.


@login_required(login_url='login')
def success_page(request):
    return render(request, 'success.html', {'data': 'Something'})


def registerView(request):

    if request.user.is_authenticated:
        return redirect('User landing page')
    else:
        form = UserCreationForm()

        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, f"Account successfully created for {user}")
                return redirect('login')

    context = {'form': form}
    return render(request, 'register.html', context)


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
