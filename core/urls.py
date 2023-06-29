from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import HomePage
from . import views


urlpatterns = [
   path('', HomePage.as_view(), name='homepage'),
   path('shop', views.marketPlace, name='market'),
   path('category/<slug:slug>', views.marketCategory, name='shop'),
   path('users/cart', views.getCartItems, name='cart'),
   path('users/cart/delete', views.delCartItem, name='del-cart-item'),
   path('users/wishlist/delete', views.delWishlistItem, name='del-wishlist-item'),
   path('users/cart', views.cartPage, name='cart-page'),
   path('users/wishlist', views.wishListPage, name='wishlist'),
   path('users/checkout', views.checkout, name='checkout'),
   path('products/<slug:slug>', views.getProduct, name='product'),
   path('products/add-to-cart', csrf_exempt(views.addCartItem), name='add-cart'),

   path('search', views.searchProducts, name='search'),
   path('contact', views.contact, name='contact'),
   path('faqs', views.faqs, name='faq'),
   path('about-us', views.aboutUs, name='about'),

]
