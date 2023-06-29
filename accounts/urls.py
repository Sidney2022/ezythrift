
from django.urls import path
from .views import SignIn, SignOut, SignUp, EmailValidationView, PasswordValidationView, UsernameValidationView
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    # authentication
    path('signup', SignUp.as_view(), name='signup'),
    path('signin', SignIn.as_view(), name='login'),
    path('logout', SignOut.as_view(), name='logout'), 
    path('reset-password', views.reset_password, name='reset-pw'),
    # validations
    path('val-user', UsernameValidationView.as_view(), name='validate-username'),
    path('val-email', EmailValidationView.as_view(), name='validate-email'),
    path('val-pw', PasswordValidationView.as_view(), name='validate-pw'),    
]
