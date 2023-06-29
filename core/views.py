from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Product, Category, SubCategory, ProductType, Cart, WishList
from django.core.paginator import Paginator
from django.http import JsonResponse


class HomePage(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        return render(request, 'main/index.html', {"products":products})


def marketCategory(request, slug):
    filter_category = Category.objects.filter(slug=slug).first()
    products = Product.objects.filter(category=filter_category, status='approved')
    if not filter_category:
        filter_category= SubCategory.objects.filter(slug=slug).first() 
        products = Product.objects.filter(sub_category=filter_category, status='approved')
        if not filter_category:
            filter_category= ProductType.objects.filter(slug=slug).first()            
            products = Product.objects.filter(product_type=filter_category, status='approved')
            if not filter_category:
                products = Product.objects.all()
                
    page_number = request.GET.get('page')
    paginator = Paginator(products, 20)
    page = paginator.get_page( page_number)
    context = {
            "products":products,
            'page':page,
    }
    return render(request, 'main/shop.html', context)


def marketPlace(request):
    products = Product.objects.filter(status='approved')
    page_number = request.GET.get('page')
    paginator = Paginator(products, 20)
    page = paginator.get_page( page_number)
    context = {
            "products":products,
            'page':page,
    }
    return render(request, 'main/shop.html', context)


def getProduct(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'main/product.html', {"product":product})


def error_404(request, exception):
    return render(request, 'main/404.html')


def addCartItem(request):
    slug = request.GET.get('slug')
    print(slug)
    print(slug.strip())
    product = get_object_or_404(Product, slug=slug)
    try:
        item  = Cart.objects.get(user=request.user, product=product)
        item.number_of_items += float(quantity)
    except Exception as e:
        print(e)
        item = Cart.objects.create(product=product, user=request.user, number_of_items=quantity)
    item.save()
    if request.method == 'POST':
        print(request.POST)
        quantity = request.POST['quantity']
        # product = request.GET['product']
        product = get_object_or_404(Product, slug=slug)
        try:
            item  = Cart.objects.get(user=request.user, product=product)
            item.number_of_items += float(quantity)
        except Exception as e:
            print(e)
            item = Cart.objects.create(product=product, user=request.user, number_of_items=quantity)
        item.save()

  
    return JsonResponse({"status":200})
    

def getCartItems(request):
    cart_items = Cart.objects.filter(user=request.user)
    number_of_items = 0
    total_amt = 0
    for item in cart_items:
        total_amt += item.product.price
        number_of_items += item.number_of_items
    return JsonResponse({"cart":list(cart_items.values()), 'number_of_items':number_of_items, "total_amt":total_amt})


def cartPage(request):
    return render(request, 'main/cart-page.html')


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
    if request.method == 'POST':
        search_str = request.POST['searchText']
        products = Product.objects.filter( name__icontains=search_str, status='approved' )
        return render(request, 'main/shop.html', {"products":products})