from django.urls import path
from .views import *


urlpatterns = [

    path('',SellerStoreList.as_view(), name='store_list'),
    path('create-store',CreateStore.as_view(), name='create_store'),
    path('delete-store/<pk>',DeleteStore.as_view(), name='delete_store'),
    path('edit-store/<pk>',EditStore.as_view(), name='edit_store'),
    path('product-list',SellerProductList.as_view(), name='product_list'),
    path('add-product',AddProduct.as_view(), name='add_product'),
    path('basket-list/<pk>',StoreBasketList.as_view(), name='basket_list'),
    path('basket-detail/<pk>',BasketDetail.as_view(), name='basket_detail'),
    path('basket_update/<pk>',UpdateBasketStatus.as_view(), name='basket_update'),

    path('profile/<pk>',SellerProfile.as_view(), name='profile'),



    path('chart/<pk>',ChartView.as_view(), name='store_chart'),
    # path("search", SearchView.as_view(), name="search"),



]