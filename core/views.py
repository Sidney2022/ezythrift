from .models import Product, Category, SubCategory, ProductType, Cart, WishList, NewsLetter, Review, Brand, Order,OrderItem, BannerProduct, Faq
from django.http import JsonResponse, HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from core.utils import SendEmail
from django.db.models import Q
from django.views import View
import requests
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseNotAllowed


def checkSort(query, products):
    if query:
        try:
            products = products.order_by(query)
        except Exception as e:
            pass 
    return products
   

class HomePage(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.filter( status='approved')
        context={
            "latest_products":products.order_by('-date')[:20],
            "hot_products":products.order_by('-no_sold')[:20],
            "products":products,
            "banners":BannerProduct.objects.all(),
            
        }
        return render(request, 'main/index.html', context)


def marketPlace(request):
    query=request.GET.get("sort")
    products = Product.objects.filter(status='approved')
    page_number = request.GET.get('page')
    items_per_page = 20
    paginator = Paginator(checkSort(query, products), items_per_page)
    page = paginator.get_page( page_number)
    start_index = (page.number - 1) * items_per_page + 1
    end_index = min(start_index + items_per_page - 1, page.paginator.count)

    context = {
            "products":products,
            'page':page,
            'start_index': start_index,
            'end_index': end_index,
            "brands":Brand.objects.all(),
            "sort_query":query
    }
    return render(request, 'main/shop.html', context)


def marketCategory(request, slug):
    query=request.GET.get("sort")
    filter_category = Category.objects.filter(slug=slug).first()
    if filter_category:
        products = Product.objects.filter(category=filter_category, status='approved')
        brands = Brand.objects.filter(category=filter_category)
    elif SubCategory.objects.filter(slug=slug).exists():
        filter_category= SubCategory.objects.filter(slug=slug).first() 
        brands = Brand.objects.filter(category=filter_category.category)
        products = Product.objects.filter(sub_category=filter_category, status='approved')
    elif ProductType.objects.filter(slug=slug).exists() :
        filter_category = ProductType.objects.filter(slug=slug).first()
        brands = Brand.objects.filter(category=filter_category.sub_category.category)
        products = Product.objects.filter(product_type=filter_category, status='approved')
    else:
        raise Http404("invalid category")
                
    page_number = request.GET.get('page')
    items_per_page = 20
    paginator = Paginator(checkSort(query, products), items_per_page)
    page = paginator.get_page( page_number)
    start_index = (page.number - 1) * items_per_page + 1
    end_index = min(start_index + items_per_page - 1, page.paginator.count)

    context = {
            "products":products,
            'page':page,
            'start_index': start_index,
            'end_index': end_index,
            "brands":brands,
            "sort_query":query
            

    }
    return render(request, 'main/shop.html', context)


def getProduct(request, slug):
    product = get_object_or_404(Product, slug=slug, status='approved')
    products = Product.objects.filter( Q(category=product.category, status='approved') | Q(brand=product.brand, status='approved')).exclude(slug=slug)
    context = {
        "product":product,
        "products":products,
        "reviews":Review.objects.filter(product=product),
        }
    if request.user.is_authenticated:
        context["can_write_review"] = product.can_write_review(product=product, request_user=request.user) 
    return render(request, 'main/product.html', context)


def error_404(request, exception):
    return render(request, 'main/404.html')


def error_500(request):
    return render(request, 'main/500.html')


@login_required()
def addCartItem(request):
    slug = request.GET.get('slug')
    product = get_object_or_404(Product, slug=slug.strip(), status='approved')
    if Cart.objects.filter(user=request.user, product=product).exists():
        return JsonResponse({"status":400})
    item  = Cart.objects.create(user=request.user, product=product)
    item.save()
    item = Cart.objects.filter(user=request.user, product=product).first()
    return JsonResponse({
            "product_name":item.product.name,
            "img":item.product.img1.url,
            "price":item.product.price,
            "quantity":item.number_of_items,
            "slug":item.product.slug
        })


@login_required()
def UpdateCartItem(request, id):
    quantity = request.GET.get('p')
    if not Cart.objects.filter(id=id, user=request.user).exists():
         return JsonResponse({ "error":"cart item could not be updated"})
    item  = get_object_or_404(Cart, id=id, user=request.user)
    if not item.product.in_stock():
        return JsonResponse({"error":"out of stock"})
    elif item.product.in_stock() and item.product.no_stock < int(quantity):
        return JsonResponse({"error":f"please retry with a lesser quantity. there are only {item.product.no_stock} units left"})
    item.number_of_items = int(quantity)
    item.save()
    total = 0
    cart_items =Cart.objects.filter(user=request.user)
    for item in cart_items:
        if item.product.in_stock():
            total += item.CartTotal()
    return JsonResponse({ "info":"cart item updated successfully", "total":total})


@login_required()
def addWishListItem(request):
    slug = request.GET.get('slug')
    product = get_object_or_404(Product, slug=slug.strip(), status='approved')
    if WishList.objects.filter(user=request.user, product=product).exists():
        return JsonResponse({"status":400})
    item  = WishList.objects.create(user=request.user, product=product)
    item.save()
    number_of_items =  len(WishList.objects.filter(user=request.user))
    return JsonResponse({"status":200, "number_of_items":number_of_items})
    

@login_required()
def getCartItems(request):
    cart_items = Cart.objects.filter(user=request.user)
    items  = [{
            "product_name":item.product.name,
            "img":item.product.img1.url,
            "price":item.product.price if item.product.discount == 0 else item.product.discount_price,
            "quantity":item.number_of_items,
            "slug":item.product.slug
        } for item in cart_items]
   
    total_amt = 0
    for item in cart_items:
        if item.product.in_stock():
            total_amt += item.CartTotal()
    #     number_of_items += item.number_of_items
    return JsonResponse({"cart":items, 'number_of_items':len(cart_items), "total_amt":total_amt})


@login_required()
def cartPage(request):
    total = 0
    cart_items =Cart.objects.filter(user=request.user)
    for item in cart_items:
        if item.product.in_stock():
            total += item.CartTotal()
    products = Product.objects.filter(status='approved')
    return render(request, 'main/cart-page.html', { "products":products, "total":total})


@login_required()
def wishListPage(request):
    return render(request, 'main/wishlist.html')


@login_required()
def checkout(request):
    if request.user.state.strip() == '' or request.user.city.strip() == '':
        messages.info(request, 'Shipping details not set. Set delivery/shipping info and then proceed to checkout')
        return redirect('account')
    elif len(Cart.objects.filter(user=request.user)) == 0:
        messages.info(request, 'you do not have any items to checkout!')
        return redirect('market')
    order_total = 0
    cart_items =  Cart.objects.filter(user=request.user)
    for item in cart_items:
        if item.product.in_stock():
            order_total += item.CartTotal()
    payable_amt = order_total + (order_total * 0.015)
        
    return render(request, 'main/checkout.html', {"payable_amt":payable_amt, "order_total":order_total})


@login_required()
def delCartItem(request):
    slug = request.GET.get('item')
    product = get_object_or_404(Product, slug=slug.strip())
    cart_item = get_object_or_404(Cart, product=product, user=request.user)
    cart_item.delete()
    return JsonResponse({"success":"item deleted"})


@login_required()
def delWishlistItem(request):
    slug = request.GET.get('item')
    product = get_object_or_404(Product, slug=slug.strip())
    wishlist_item = get_object_or_404(WishList, product=product, user=request.user)
    wishlist_item.delete()
    return JsonResponse({"success":"item deleted"})


def searchProducts(request):
    search_str = request.GET['item']
    sort_query = request.GET['sort']
    products = Product.objects.filter( name__icontains=search_str, status='approved' )
    page_number = request.GET.get('page')
    items_per_page = 20
    paginator = Paginator(checkSort(sort_query, products), items_per_page)
    page = paginator.get_page( page_number)
    start_index = (page.number - 1) * items_per_page + 1
    end_index = min(start_index + items_per_page - 1, page.paginator.count)
    context = {
            "products":products,
            'page':page,
            "item":search_str,
            "brands":Brand.objects.all(),
            "sort_query":sort_query,
            'start_index': start_index,
            'end_index': end_index,
            "item":search_str
    }
    return render(request, 'main/shop.html', context)


def newsLetter(request):
    if request.method =="POST":
        email = request.POST['email']
        if  NewsLetter.objects.filter(email=email).exists() or not email:
            return JsonResponse({"status":'error'})
        new_email = NewsLetter.objects.create(email=email)
        new_email.save()
        return JsonResponse({"status":'success'})


@login_required()
def writeReview(request, slug):
    if request.method == 'POST':
        review = request.POST['comment']
        rating = request.POST['rating']
        product = get_object_or_404(Product, slug=slug, status='approved')
        if not product.can_write_review(product=product, request_user=request.user):
            messages.error(request, 'you cannot write a review because you have not purchased product')
            return redirect('product', slug) 
        new_review = Review.objects.create(user=request.user, product=product, rating=rating, review=review)
        new_review.save()
        messages.success(request, 'review added successfully')
        return redirect('product', slug)
    raise Http404('invalid request')

    

@login_required()
def createOrder(request, id):
    # only after successful payment
    order = get_object_or_404(Order, tracking_id=id)
    cart_items = Cart.objects.filter(user=request.user)
    for item in cart_items:
        if item.product.discount == 0:
            amount = item.number_of_items * item.product.price
            unit_price = item.product.price
        else:
            amount = item.number_of_items * item.product.discount_price
            unit_price = item.product.discount_price
        new_order_item = OrderItem.objects.create(user=item.user, order=order, product=item.product, quantity=item.number_of_items, amount=amount, unit_price=unit_price)
        new_order_item.save()
        product = Product.objects.get(slug=item.product.slug)
        product.no_stock -= item.number_of_items # calculate the product quantity ordered, and deduct from available_stock
        product.save()
        item.delete()
    return redirect('account')


@login_required()
def getOrderItems(request, pk):
    order = get_object_or_404(Order, tracking_id=pk)
    order_items = OrderItem.objects.filter(order=order)
    page_number = request.GET.get('page')
    paginator = Paginator(order_items, 20)
    page = paginator.get_page( page_number)
    context = {
            'page':page,
            "order_items":order_items,
            "order":order
    }
    return render(request, 'main/orders.html', context)
    

def payment_success(request, id ):
    return HttpResponse(f"{id}")


@login_required()
def payment(request):
    try:
        order_amt = 0
        cart_items =  Cart.objects.filter(user=request.user)
        for item in cart_items:
            order_amt +=  item.CartTotal()
        # # Set up the API endpoint and headers
        order = Order.objects.create(user=request.user)
        order.save()
        url = 'https://api.paystack.co/transaction/initialize'
        headers = {
            'Authorization': 'Bearer sk_test_8f1d2a9288296f690d843434b760a147a8353bb2',
            'Content-Type': 'application/json'
        }
        # Set up the request payload
        amt= order_amt * 100
        payload = {
            'amount':amt + (amt*0.015) ,  # Amount in kobo (e.g., 5000 Naira)
            'email': request.user.email,
            'callback_url': request.build_absolute_uri(f'/place-order/{order.tracking_id}'),
            'channels': ['card'],
            'reference': f'{order.tracking_id}'  # Set the custom reference
        }
        # Send the API request
        response = requests.post(url, json=payload, headers=headers)
        # Handle the API response
        if response.status_code == 200:
            data = response.json()
            authorization_url = data['data']['authorization_url']
            return redirect(authorization_url)
        else:
            # Handle the error response
            return HttpResponse(response.text, status=response.status_code)
    except Exception as e:
        print(e)
        raise Http404("poor network")


def mail(request):
    SendEmail("Test", ["ezythrift@gmail.com"])
    return JsonResponse({"ok":""})


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        if name and email and subject and message:
            context ={
                "name":name,
                "message":message
            }
            e = SendEmail(subject, settings.DEFAULT_FROM_EMAIL,context,'emails/contact.html' )
            print(e)
            messages.success(request, 'email sent successfully, or failed')
            return redirect('contact')
        else:
            messages.error(request, 'fields can not be blank')
            return redirect('contact')
    return render(request, 'main/contact.html')


def faqs(request):
    return render(request, 'main/faq.html', {"faqs":Faq.objects.all()})


def aboutUs(request):
    return render(request, 'main/about.html')


def terms_and_conditions(request):
    return render(request, 'main/terms.html')

def privacy_policy(request):
    return render(request, 'main/policy.html')