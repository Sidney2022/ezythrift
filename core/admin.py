from .models import Product, Category, SubCategory, Review, Cart, Brand, ProductType, Seller, WishList, NewsLetter, Order, OrderItem, BannerProduct, Faq
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django import forms

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name',  'category', 'date', 'status', 'price', 'discount_price', 'no_stock', 'in_stock', "Edit_button", 'delete_button']
    search_fields = ['name', 'description']  # Fields to be searched
    readonly_fields = []  # Fields that should be read-only for all users
    list_per_page = 20
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'seller' and not request.user.is_superuser:
            seller_obj = Seller.objects.get(profile=request.user)
            kwargs['initial'] = seller_obj
            kwargs['widget'] = forms.HiddenInput()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if not request.user.is_superuser:
            read_only = ['status', 'discount_price', 'price', 'no_reviews', 'no_sold']
            fieldsets[0][1]['fields'] = tuple(
                field for field in fieldsets[0][1]['fields'] if not field in read_only
            )
        return fieldsets


    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            # Hide the 'status' field for non-superusers
            return self.readonly_fields + ['status']
        return self.readonly_fields
    
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        # Custom search logic
        queryset |= self.model.objects.filter(description__icontains=search_term)  # Add additional search fields as needed
        return queryset, use_distinct
    
    def delete_button(self, obj):
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.pk])
        return format_html(
            '<a style="display: inline-block; padding: 6px 12px;background-color: #dc3545; color: #fff;text-decoration: none;border-radius: 4px;" class="button" href="{}">Delete</a>', delete_url)

    delete_button.short_description = ''

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.only('pk')  # Optimize queryset by selecting only the primary key
        return qs
    
    def Edit_button(self, obj):
        return format_html('<a style="display: inline-block; padding: 6px 12px;background-color: teal; color: #fff;text-decoration: none;border-radius: 4px;"  class="button btn-warning" href="{}">Edit</a>', obj.pk)

    Edit_button.short_description = 'Actions'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['slug',  'category']

class CartAdmin(admin.ModelAdmin):
    list_display = ['user',  'product', 'number_of_items', 'CartTotal', 'timestamp']

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['user',  'product', 'quantity', 'order']

class WishListAdmin(admin.ModelAdmin):
    list_display = ['user',  'product']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'tracking_id', 'status', 'date', 'items']

class BrandAdmin(admin.ModelAdmin):
    list_display = ['brand',  'category']

class BannerProductAdmin(admin.ModelAdmin):
    list_display = ['product',  'role']

class FaqAdmin(admin.ModelAdmin):
    list_display = ['question']

admin.site.register(Faq, FaqAdmin)
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
admin.site.register(BannerProduct, BannerProductAdmin)
