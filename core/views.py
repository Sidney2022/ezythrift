from .models import Product, Category, SubCategory, ProductType, Cart, WishList, NewsLetter, Review, Brand, Order,OrderItem
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from django.views import View


class HomePage(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        return render(request, 'main/index.html', {"products":products})


def marketPlace(request):
    products = Product.objects.filter(status='approved')
    page_number = request.GET.get('page')
    
    paginator = Paginator(products, 20)
    page = paginator.get_page( page_number)
    context = {
            "products":products,
            'page':page,
            "brands":Brand.objects.all(),
    }
    return render(request, 'main/shop.html', context)


def marketCategory(request, slug):
    filter_category = Category.objects.filter(slug=slug).first()
    products = Product.objects.filter(category=filter_category, status='approved')
    brands = Brand.objects.filter(category=filter_category)
    if not filter_category:
        filter_category= SubCategory.objects.filter(slug=slug).first() 
        brands = Brand.objects.filter(category=filter_category.category)
        products = Product.objects.filter(sub_category=filter_category, status='approved')
        if not filter_category:
            filter_category= ProductType.objects.filter(slug=slug).first()  
            print(filter_category)          
            brands = Brand.objects.filter(category=filter_category.sub_category.category)
            products = Product.objects.filter(product_type=filter_category, status='approved')
            if not filter_category:
                brands = Brand.objects.all()
                products = Product.objects.all()
                
    page_number = request.GET.get('page')
    paginator = Paginator(products, 20)
    page = paginator.get_page( page_number)
    context = {
            "products":products,
            'page':page,
            "brands":brands
            

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
    

def addWishListItem(request):
    slug = request.GET.get('slug')
    product = get_object_or_404(Product, slug=slug.strip(), status='approved')
    if WishList.objects.filter(user=request.user, product=product).exists():
        return JsonResponse({"status":400})
    item  = WishList.objects.create(user=request.user, product=product)
    item.save()
    return JsonResponse({"status":200})
    

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
        number_of_items += item.number_of_items
    return JsonResponse({"cart":items, 'number_of_items':number_of_items, "total_amt":total_amt})


def cartPage(request):
    cart_items =Cart.objects.filter(user=request.user)
    no_items = 0
    for item in cart_items:
        no_items += (item.product.price * item.number_of_items)
       
    return render(request, 'main/cart-page.html', {"no_items":no_items})


def wishListPage(request):
    return render(request, 'main/wishlist.html')


def checkout(request):
    return render(request, 'main/checkout.html')


def delCartItem(request):
    slug = request.GET.get('item')
    product = get_object_or_404(Product, slug=slug.strip())
    cart_item = get_object_or_404(Cart, product=product, user=request.user)
    cart_item.delete()
    return JsonResponse({"success":"item deleted"})


def delWishlistItem(request):
    slug = request.GET.get('item')
    product = get_object_or_404(Product, slug=slug.strip())
    wishlist_item = get_object_or_404(WishList, product=product, user=request.user)
    wishlist_item.delete()
    return JsonResponse({"success":"item deleted"})


def contact(request):
    return render(request, 'main/contact.html')


def faqs(request):
    return render(request, 'main/faq.html')


def aboutUs(request):
    return render(request, 'main/about.html')


def searchProducts(request):
    search_str = request.GET['item']
    products = Product.objects.filter( name__icontains=search_str, status='approved' )
    page_number = request.GET.get('page')
    paginator = Paginator(products, 20)
    page = paginator.get_page( page_number)
    context = {
            "products":products,
            'page':page,
            "item":search_str,
            "brands":Brand.objects.all()
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


def writeReview(request, slug):
    if request.method == 'POST':
        review = request.POST['comment']
        rating = request.POST['rating']
        product = get_object_or_404(Product, slug=slug, status='approved')
        new_review = Review.objects.create(user=request.user, product=product, rating=rating, review=review)
        new_review.save()
        return JsonResponse({"status":200})
    

def createOrder(request):
    # only after successful payment
    order = Order.objects.create(user=request.user, status="in progress")
    order.save()
    print(order)
    # cart_items = Cart.objects.filter(user=request.user)
    # for item in cart_items:
    #     new_order_item = OrderItem.objects.create(user=item.user, product=item.product, quantity=item.number_of_items)
    #     new_order_item.save()
    #     item.delete()
    return redirect('cart-page')
    