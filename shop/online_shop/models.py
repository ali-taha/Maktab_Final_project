from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from random import randint
import datetime


User = get_user_model()

class ProductCategory(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=50,unique=True)
    description = models.TextField()
    slug = models.SlugField(unique=True)
    
    class Meta:
        ordering = ['title']


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(ProductCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class ProductTag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['title']


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(ProductTag, self).save(*args, **kwargs)

    def __str__(self):
        return self.title    


class StoreType(models.Model):
    title = models.CharField(max_length=50) 
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['title']


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(StoreType, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class ExcludeDeletedStores(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(status=DEL)
      
REV = 'rev'
CON = 'con'
DEL = 'del'
STORE_STATUS_CHOICES = [
        (REV,'Review mode'),
        (CON,'Confirmed mode'),
        (DEL,'Deleted mode'),
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

    objects = models.Manager()
    alive = ExcludeDeletedStores()

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.title

    def delete(self):
        self.status = DEL
        self.save()
        pass    


class AvailableProduct(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(stock=0)


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

    objects = models.Manager()
    available = AvailableProduct()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        qs = Product.objects.filter(slug=self.slug)
        exists = qs.exists()
        while exists:
            randumber = randint(1, 1000)
            new_slug = self.slug + str(randumber)
            self.slug = slugify(new_slug)
            qs = Product.objects.filter(slug=self.slug)
            exists = qs.exists()
        return super(Product, self).save(*args, **kwargs)

    class Meta:
        ordering = ['pk']    


CON = 'con'
REV = 'rev'
CAN = 'can'
PAI = 'pai'
BASKET_STATUS_CHOICES = [
        (CON,'Confirmed'),
        (REV,'Review'),
        (CAN,'Canceled'),
        (PAI,'Paid'),
    ]             

class Basket(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.PROTECT, null=True)
    total_price = models.IntegerField(default=0)
    count_items = models.IntegerField(default=0)
    status = models.CharField(max_length=3,choices=BASKET_STATUS_CHOICES,default=REV)
    created_on = models.DateTimeField(auto_now_add=True , null=True)
    updated_on = models.DateTimeField(auto_now=True , null=True)
    paid_on = models.DateTimeField(null=True,blank=True)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return str(self.id)    


class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    buy_price = models.IntegerField(default=0)

    class Meta:
        ordering = ['basket']

    def save(self, *args, **kwargs):
        price = self.product.price
        if self.product.stock >= self.count:
            self.basket.total_price += (self.count * price)
            self.basket.count_items += self.count
            self.buy_price = price
            self.basket.save()
            self.product.stock = self.product.stock - self.count
            self.product.save()
            super(BasketItem, self).save(*args, **kwargs)

    def delete(self):
     basketitem = BasketItem.objects.get(id=self.id)
     price = self.product.price
     if basketitem:
            self.product.stock = self.product.stock + self.count
            self.product.save()
            self.basket.total_price -= (self.count * price)
            self.basket.count_items -= self.count
            if self.basket.count_items == 0:
                self.basket.delete()
            else:    
                self.basket.save()
     super(BasketItem, self).delete()    

 
