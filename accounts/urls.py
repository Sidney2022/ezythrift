
from django.urls import path
from .views import SignIn, SignOut, SignUp, EmailValidationView, PasswordValidationView, UsernameValidationView

from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # authentication
    # path('signup', SignUp.as_view(), name='signup'),
    # path('signin', SignIn.as_view(), name='login'),
    path('logout', SignOut.as_view(), name='logout'), 
    path('reset-password', views.reset_password, name='reset-pw'),
    # validations
    path('val-user', UsernameValidationView.as_view(), name='validate-username'),
    path('val-email', EmailValidationView.as_view(), name='validate-email'),
    path('val-pw', PasswordValidationView.as_view(), name='validate-pw'),    

    path("", views.accountPage, name='account'),
    path("auth", views.AuthPage, name='auth'),
    path("signup", csrf_exempt(views.register), name='signup'),
    path("signin", csrf_exempt(views.login), name='signin'),

    path('shipping', views.editShippingDetail, name='shipping'),
    path('change-password', views.changePw, name='change-pw'),

]
