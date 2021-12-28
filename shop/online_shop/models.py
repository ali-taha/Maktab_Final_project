from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from random import randint


User = get_user_model()

class ProductCategory(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=50,unique=True)
    description = models.TextField()
    slug = models.SlugField(unique=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(ProductCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class ProductTag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(ProductTag, self).save(*args, **kwargs)


class StoreType(models.Model):
    title = models.CharField(max_length=50) 
    slug = models.SlugField(unique=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(StoreType, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

REV = 'rev'
REG = 'reg'
DEL = 'del'
STORE_STATUS_CHOICES = [
        (REV,'review_mode'),
        (REG,'registered_mode'),
        (DEL,'deleted_mode'),
    ]        
   
class Store(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    status = models.CharField(max_length=3,choices=STORE_STATUS_CHOICES,default=REV)
    type = models.ForeignKey(StoreType,on_delete=models.SET_NULL , null=True)
    description = models.TextField()
    location_lat = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    location_lng =  models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Store, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    tag = models.ManyToManyField(ProductTag,blank=True)
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to="uploads/shop")
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    price = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        qs = ProductCategory.objects.filter(slug=self.slug)
        exists = qs.exists()
        while exists:
            randumber = randint(1, 1000)
            new_slug = self.slug + str(randumber)
            self.slug = slugify(new_slug)
            qs = ProductCategory.objects.filter(slug=self.slug)
            exists = qs.exists()
        return super(ProductCategory, self).save(*args, **kwargs)


CON = 'con'
REV = 'rev'
CAN = 'can'
PAI = 'pai'
BASKET_STATUS_CHOICES = [
        (CON,'confirmed'),
        (REV,'review'),
        (CAN,'canceled'),
        (PAI,'paid'),
    ]             

class Basket(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.PROTECT, null=True)
    total_price = models.IntegerField(default=0)
    status = models.CharField(max_length=3,choices=STORE_STATUS_CHOICES,default=REV)
    paid_on = models.DateTimeField(null=True,blank=True)

    class Meta:
        ordering = ['paid_on']

    def __str__(self):
        return self.owner

class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.basket