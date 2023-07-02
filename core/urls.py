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
   path('users/checkout', views.checkout, name='checkout'),

   path('users/wishlist-items', views.wishListPage, name='wishlist'),
   path('users/cart-items', views.cartPage, name='cart-page'),

   path('products/<slug:slug>', views.getProduct, name='product'),

   path('users/add-to-cart', views.addCartItem, name='add-cart'),
   path('users/add-to-wishlist', views.addWishListItem, name='add-wishlist'),

   path('search', views.searchProducts, name='search'),
   path('contact', views.contact, name='contact'),
   path('faqs', views.faqs, name='faq'),
   path('about-us', views.aboutUs, name='about'),
   path('newsletter', views.newsLetter, name='newsletter'),
   path('products/<slug:slug>/review', views.writeReview, name='review'),

   path('place-order', views.createOrder, name="order")


]
