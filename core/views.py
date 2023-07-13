from .models import Product, Category, SubCategory, ProductType, Cart, WishList, NewsLetter, Review, Brand, Order,OrderItem, BannerProduct
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
    products = Product.objects.filter( Q(category=product.category) | Q(brand=product.brand)).exclude(slug=slug)
    context = {
        "product":product,
        "products":products
        }
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
    quantity = request.GET.get('quantity')
    print(quantity, id)
    item  = get_object_or_404(Cart, id=id)
    print(item)
    item.number_of_items += int(quantity)
    item.save()
    return JsonResponse({
            "info":"cart item updated successfully"
        })


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
    number_of_items = 0
    items  = [{
            "product_name":item.product.name,
            "img":item.product.img1.url,
            "price":item.product.price,
            "quantity":item.number_of_items,
            "slug":item.product.slug
        } for item in cart_items]
   
    total_amt = 0
    for item in cart_items:
        total_amt += item.product.price
    #     number_of_items += item.number_of_items
    return JsonResponse({"cart":items, 'number_of_items':len(cart_items), "total_amt":total_amt})


@login_required()
def cartPage(request):
    cart_items =Cart.objects.filter(user=request.user)
    no_items = 0
    for item in cart_items:
        no_items += (item.product.price * item.number_of_items)
       
    return render(request, 'main/cart-page.html', {"no_items":no_items})


@login_required()
def wishListPage(request):
    return render(request, 'main/wishlist.html')


@login_required()
def checkout(request):
    order_amt = 0
    cart_items =  Cart.objects.filter(user=request.user)
    for item in cart_items:
        order_amt += (item.number_of_items * item.product.price) 
        
    return render(request, 'main/checkout.html', )


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
    return render(request, 'main/faq.html')


def aboutUs(request):
    return render(request, 'main/about.html')


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
        new_review = Review.objects.create(user=request.user, product=product, rating=rating, review=review)
        new_review.save()
        return redirect('product', slug)
    

@login_required()
def createOrder(request, id):
    # only after successful payment
    order = get_object_or_404(Order, tracking_id=id)

    cart_items = Cart.objects.filter(user=request.user)
    for item in cart_items:
        new_order_item = OrderItem.objects.create(user=item.user, order=order, product=item.product, quantity=item.number_of_items)
        new_order_item.save()
        product = Product.objects.get(slug=item.product.slug)
        product.no_stock -= item.number_of_items
        product.save()
        item.delete()
    # also calculate the product quantity, and deduct from no_stock
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
            order_amt += (item.number_of_items * item.product.price) 
        # # Set up the API endpoint and headers
        order = Order.objects.create(user=request.user)
        order.save()
        url = 'https://api.paystack.co/transaction/initialize'
        headers = {
            'Authorization': 'Bearer sk_test_8f1d2a9288296f690d843434b760a147a8353bb2',
            'Content-Type': 'application/json'
        }
        # Set up the request payload
        payload = {
            'amount': order_amt * 100,  # Amount in kobo (e.g., 5000 Naira)
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

