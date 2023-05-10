from django.urls import path, include
from .views import success_page, registerView, loginView, logoutView


urlpatterns = [
    path('success', success_page, name='User landing page'),
    path('register', registerView, name="register"),
    path('login', loginView, name="login"),
    path('logout', logoutView, name='logout'),

]
