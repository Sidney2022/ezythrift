from django.contrib import admin

from .models import Product, Category, SubCategory, Review, Cart, Brand, ProductType, Seller, WishList


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name',  'category', 'slug', 'status']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['slug',  'category']

class CartAdmin(admin.ModelAdmin):
    list_display = ['user',  'product', 'number_of_items']

class WishListAdmin(admin.ModelAdmin):
    list_display = ['user',  'product']

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductType, )
admin.site.register(Seller, )
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory)
admin.site.register(Review)
admin.site.register(Brand)
admin.site.register(Cart, CartAdmin)
admin.site.register(WishList, WishListAdmin)
