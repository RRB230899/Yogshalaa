from django.urls import path, include
from .views import success_page, registerView, loginView, logoutView, verifyOTP, coverageView, create_checkout_session


urlpatterns = [
    path('success', success_page, name='User Landing Page'),
    path('register', registerView, name="register"),
    path('otp/<str:uid>/', verifyOTP, name='otp'),
    path('login', loginView, name="login"),
    path('logout', logoutView, name='logout'),
    path('coverage', coverageView, name="Coverage"),
    path('create-checkout-session', create_checkout_session, name='Checkout session')
]
