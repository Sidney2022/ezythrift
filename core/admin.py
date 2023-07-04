from django.contrib import admin

from .models import Product, Category, SubCategory, Review, Cart, Brand, ProductType, Seller, WishList, NewsLetter, Order, OrderItem


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name',  'category', 'slug', 'status', 'sub_category', 'product_type', 'no_stock', 'is_in_stock']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['slug',  'category']

class CartAdmin(admin.ModelAdmin):
    list_display = ['user',  'product', 'number_of_items', 'timestamp']

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['user',  'product', 'quantity', 'order']

class WishListAdmin(admin.ModelAdmin):
    list_display = ['user',  'product']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'tracking_id', 'status', 'date', 'items']

class BrandAdmin(admin.ModelAdmin):
    list_display = ['brand',  'category']

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductType, )
admin.site.register(Seller, )
admin.site.register(NewsLetter, )
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory)
admin.site.register(Review)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Brand)
admin.site.register(Cart, CartAdmin)
admin.site.register(WishList, WishListAdmin)
