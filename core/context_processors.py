from .models import Category, ProductType, Brand, Cart, WishList


def ProductCategories(request):
    context =  {
        "product_categories":Category.objects.all(), 
        "product_types":ProductType.objects.all(),
        }
    if request.user.is_authenticated:
        order_amt = 0
        cart_items =  Cart.objects.filter(user=request.user)
        for item in cart_items:
            order_amt += (item.number_of_items * item.product.price) 
        context['cart_items'] = Cart.objects.filter(user=request.user)
        context['wishlist_items'] = WishList.objects.filter(user=request.user)
        context['order_amt'] =order_amt
        context['number_of_items'] =  len(WishList.objects.filter(user=request.user))
    return context