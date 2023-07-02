from .models import Category, ProductType, Brand, Cart, WishList


def ProductCategories(request):
    context =  {
        "product_categories":Category.objects.all(), 
        "product_types":ProductType.objects.all(),
        # "brands":Brand.objects.all(),
        }
    if request.user.is_authenticated:
        cart_items = { 
            "cart": Cart.objects.filter(user=request.user),
            # number_of_items
        }
        context['cart_items'] = Cart.objects.filter(user=request.user)
        context['wishlist_items'] = WishList.objects.filter(user=request.user)
    return context