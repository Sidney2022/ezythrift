from django.db import models
from accounts.models import Profile
import uuid
from django.utils.text import slugify



class Seller(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.profile.username


class Category(models.Model):
    category = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def SubCategories(self):
        sub_categories = SubCategory.objects.filter(category=self.id)
        return sub_categories
    
    def productType(self):
        products = [product for product in self.SubCategories()]
        return 
    
    

    def __str__(self):
        return self.category
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.category)
        super(Category, self).save(*args, **kwargs)


class Brand(models.Model):
    brand = models.CharField(max_length=255)
    c = Category.objects.all().first()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=c.id)
    def __str__(self):
        return self.brand


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True)


    class Meta:
        verbose_name_plural = 'Sub categories'
         
    def __str__(self):
        return self.sub_category
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.sub_category)
        super(SubCategory, self).save(*args, **kwargs)
    

class ProductType(models.Model):
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    product_type = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.product_type
    
    def products(self):
        p = Product.objects.filter(product_type=self.product_type)
        return p

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_type)
        super(ProductType, self).save(*args, **kwargs)
    

class Product(models.Model):
    id_product = models.UUIDField(default=uuid.uuid4)
    name = models.CharField(max_length=40)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    no_stock = models.PositiveIntegerField()
    is_hot = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    img1 = models.ImageField(upload_to='products')
    img2 = models.ImageField(upload_to='products')
    img3 = models.ImageField(upload_to='products')
    img4 = models.ImageField(upload_to='products')
    img5 = models.ImageField(upload_to='products')
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(default=0)
    discount_price = models.PositiveIntegerField(null=True, blank=True)
    no_reviews = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=(
        ("under review","Under Review"),
        ("approved", "Approved"),
        ("declined", "Declined")
    ))
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(null=True, blank=True)
    no_sold =models.PositiveIntegerField(default=0) #for bestseller feature

    def reviews(self):
        reviews = Review.objects.filter(product=self.id)
        return reviews

    def save(self, *args, **kwargs):
        if not self.discount == 0:
            self.discount_price = self.price - (self.price * (self.discount/100))
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def is_in_stock(self):
        if self.no_stock != 0:
            return True
        else:
            return False
    # create color model and get it here via a method


class Review(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    review = models.TextField()
    date = models.DateTimeField(auto_now_add=True, null=True)


class Cart(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    number_of_items = models.PositiveIntegerField(default=1)
    timestamp =models.DateTimeField(null=True, auto_now_add=True)
    def cartNum(self):
        cart = 0
        for item in Cart.objects.filter(user=self.user):
            cart += item.product.price
        return cart


class WishList(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class NewsLetter(models.Model):
    email = models.EmailField()
    def __str__(self):
        return self.email


# class Billing(models.Model):
#     user = models.ForeignKey(Profile, on_delete=models.CASCADE)

# class FeaturedProduct(models.Model):
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Order(models.Model):
    tracking_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=40, choices= (
        ("in progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled")
    ), default= "in progress")
    badge = models.CharField(max_length=30, null=True,  blank=True)
    
    # at checkout, all products in cart are emptied.
   

    def save(self, *args, **kwargs):
        if self.status == 'cancelled':
            self.badge = 'danger'
        elif self.status == 'in progress':
            self.badge = 'warning'
        else:
            self.badge = 'success'
        super(Order, self).save(*args, **kwargs)


    class Meta:
        ordering = ['-date']


class OrderItem(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default = None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)


        


