from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.auth.models import auth
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.http import JsonResponse, Http404
from django.contrib import messages
from django.conf import settings
from django.views import View
from core.models import Order
from .models import Profile, Billing
import json
import os
from core.models import Cart, Product


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

        return render(request, 'accounts/auth.html', {"redirect_page":redirect_page})


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
            return render(request, 'accounts/auth.html', context)
        elif Profile.objects.filter(email=email).exists():
            messages.error(request, 'email already exists')
            return render(request, 'accounts/auth.html', context)
        elif password != password2:
            messages.error(request, 'passwords do not match!')
            return render(request, 'accounts/auth.html', context)

        try:
            validate_password(password)
            new_user = Profile.objects.create_user(username=username, email=email, password=password)
            new_user.save()
            auth.authenticate(username=username, password=password)
            auth.login(request, new_user)
            return redirect("homepage")
        except Exception as e:
            messages.error(request, str(e))
            return render(request, 'accounts/auth.html', context)



    def get(self, request):
        # f = os.path.join(settings.BASE_DIR, 'currency.json')
        # with open(f, 'r', encoding='utf-8') as file:
        #     json_data = json.load(file)
        #     data = [({'name':k,'value':v['name'], 'symbol':v['symbol']}) for k,v in json_data.items()]

        # context = {
        #     'currencies':data,
        # }
        return render(request, 'accounts/auth.html')


class SignOut(View):
    def get(self, request):
        auth.logout(request)
        messages.info(request, "logged out successfuly")
        return redirect('auth')


def reset_password(request):
    return render(request, 'accounts/reset-pw.html')


@login_required()
def accountPage(request):
    orders = Order.objects.filter(user=request.user)
    context = {
        "myorders":orders
    }
    return render(request, 'accounts/account.html', context)


def register(request):
    if request.method =="POST":
        data = json.loads(request.body)
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        password = data['password']
        password2 = data['password2']
        if Profile.objects.filter(email=email).exists():
            return JsonResponse({"email_exists":'email in use'})
        elif password !=password2:
            return JsonResponse({"password_match":'passwords do not match'})
        try:
            validate_password(password)
            new_user = Profile.objects.create_user(username=email, first_name=first_name, last_name=last_name, email=email, password=password)
            new_user.save()
            from core.utils import SendEmail
            msg=f"You are welcome to Ezythrift. we are delighted to have you onboard and we hope you enjoy your shopping experience with us"
            # SendEmail("Welcome To EzyThrift", email, {"email_content":msg, "user_name":first_name},"emails/admin.html")
            user = auth.authenticate(email=email, password=password)
            auth.login(request, user)
            return JsonResponse({"success":"registration was successful"})
        except Exception as err:
            return JsonResponse({'password_strength':str(err)})
    raise Http404("invalid request")


def login(request):
    if request.method =="POST":
        data = json.loads(request.body)
        email = data['email']
        print(email)
        password = data['password']
        user = auth.authenticate(email=email, password=password)
        print(user)
        if user:
            auth.login(request, user)
            for slug, quantity in  request.session.get('cart', {}).items():
                product = get_object_or_404(Product, slug=slug)
                cart_item = Cart.objects.filter(user=request.user, product=product).first()
                if cart_item:
                    cart_item.number_of_items += quantity
                else:
                    cart_item = Cart.objects.create(user=request.user, number_of_items=quantity, product=product)
                    cart_item.save()
            return JsonResponse({"success":"logged In"})
        else:
            return JsonResponse({"auth_error":"invalid login"})
    raise Http404("invalid request")


def AuthPage(request):
    if request.user.is_authenticated:
        return redirect("homepage")
    redirect_page = request.GET.get("next")
    return render (request, 'accounts/auth.html',  {"redirect_page":redirect_page})


@login_required()
def editShippingDetail(request):
    if request.method == "POST":
        country = request.POST['country']
        town = request.POST['town']
        state = request.POST['state']
        address = request.POST['address']
        phone = request.POST['phone']
        apartment = request.POST['apartment']
        user_acct = Profile.objects.get(email=request.user.email)
        user_acct.phone_number = phone
        user_acct.country = country
        user_acct.state = state
        user_acct.city = town
        user_acct.apartment = apartment
        user_acct.address = address
        user_acct.save()
        return JsonResponse({"status":"well received and saved"})


@login_required()
def changePw(request):
    if request.method == "POST":
        profile = get_object_or_404(Profile, email=request.user.email)
        current_password = request.POST['current']
        new_pw = request.POST['password']
        new_pw2 = request.POST['password2']
        user = auth.authenticate(email=profile.email, password=current_password)
        if not user:
            return JsonResponse({"pw_incorrect":"incorrect password"})
        elif not new_pw == new_pw2:
            return JsonResponse({"pw_match":" passwords do not match"})
        try:
            validate_password(new_pw)
            profile.set_password(new_pw)
            return JsonResponse({"success":"password changed successfully"})
        except Exception as err:
            return JsonResponse({'password_strength':str(err)})


@login_required()
def billing_info(request):
    billing  = Billing.objects.filter(user=request.user).first()
    if request.method == 'POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        country=request.POST['country']
        state=request.POST['state']
        city=request.POST['city']
        address=request.POST['address']
        phone_number=request.POST['phone_number']
        # apartment=request.POST['apartment']
        profile = get_object_or_404(Profile, email=request.user.email)
        profile.first_name = first_name
        profile.last_name = last_name
        profile.save()
        if not billing:
            billing = Billing.objects.create(
                user=profile, 
                country=country,
                state=state,
                city=city,
                address =address,
                # apartment=apartment
                )
        else:
            billing.city = city
            billing.country = country
            billing.state = state
            billing.city = city
            billing.address = address
            billing.phone_number = phone_number

        billing.save()
        messages.success(request, 'billing details has been updated')
        return redirect('billing')
    return render(request, 'accounts/billing.html',{"billing":billing})