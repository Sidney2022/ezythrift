from django.contrib.auth.models import auth
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.password_validation import validate_password
from django.http import JsonResponse
import json
from .models import Profile
from django.conf import settings
import os


class SignIn(View):
    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        next_page = request.POST['next']
        print(username, password)
        user = auth.authenticate(username=username, password=password)
        print(user)
        if user:
            if user and user.is_active:
                auth.login(request, user)
                if next_page != 'None':
                    return redirect(next_page)
                else:
                    return redirect('homepage')
            else:
                messages.warning(request, 'account has not been verified')
                return redirect('login')
        else:
            messages.error(request, 'invalid login credentials')
            return redirect('login')
            
    def get(self, request, *args, **kwargs):
        redirect_page = request.GET.get("next")
        if request.user.is_authenticated:
            messages.warning(request, f'You are already logged in')
            return redirect('homepage')
        
        return render(request, 'auth/auth.html', {"redirect_page":redirect_page})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters'}, status=400)
        if Profile.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'sorry username in use,choose another one '}, status=409)
        return JsonResponse({'username_valid': True})
    

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if Profile.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'sorry email in use. If this is your account, proceed to login '}, status=409)
        return JsonResponse({'email_valid': True})
    

class PasswordValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        password = data['password']
        password2 = data['password2']
        if password != password2:
            return JsonResponse({'pw_error':"passwords do not match"})
        try:
            validate_password(password)
        except Exception as err:
            return JsonResponse({'pw_error':str(err)})
        return JsonResponse({'password_valid': True})


class SignUp(View):
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        context = { "fields": request.POST }
        if Profile.objects.filter(username=username).exists():
            messages.error(request, 'username already exists')
            return render(request, 'auth/auth.html', context)
        elif Profile.objects.filter(email=email).exists():
            messages.error(request, 'email already exists')
            return render(request, 'auth/auth.html', context)
        elif password != password2:
            messages.error(request, 'passwords do not match!')
            return render(request, 'auth/auth.html', context)
        
        try:
            validate_password(password)
            new_user = Profile.objects.create_user(username=username, email=email, password=password)
            new_user.save()
            auth.authenticate(username=username, password=password)
            auth.login(request, new_user)
            return redirect("homepage")
        except Exception as e:
            messages.error(request, str(e))
            return render(request, 'auth/auth.html', context)
    
    

    def get(self, request):
        # f = os.path.join(settings.BASE_DIR, 'currency.json')
        # with open(f, 'r', encoding='utf-8') as file:
        #     json_data = json.load(file)
        #     data = [({'name':k,'value':v['name'], 'symbol':v['symbol']}) for k,v in json_data.items()]
               
        # context = {
        #     'currencies':data,
        # }
        return render(request, 'auth/auth.html')


class SignOut(View):
    def get(self, request):
        auth.logout(request)
        messages.info(request, "logged out successfuly")
        return redirect('login')


def reset_password(request):
    return render(request, 'auth/reset-pw.html')






