from django.contrib import admin
from .models import ProductCategory, ProductTag, StoreType, Store, Product, Basket, BasketItem

admin.site.register(ProductCategory)
admin.site.register(ProductTag)
admin.site.register(StoreType)
admin.site.register(Store)
admin.site.register(Product)
admin.site.register(Basket)
admin.site.register(BasketItem)