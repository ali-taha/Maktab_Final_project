from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *


urlpatterns = [

    path('',login_required(login_url='sign_in')(SellerStoreList.as_view()), name='store_list'),
    path('create-store',login_required(login_url='sign_in')(CreateStore.as_view()), name='create_store'),
    path('delete-store/<pk>',login_required(login_url='sign_in')(DeleteStore.as_view()), name='delete_store'),
    path('edit-store/<pk>',login_required(login_url='sign_in')(EditStore.as_view()), name='edit_store'),
    path('product-list',login_required(login_url='sign_in')(SellerProductList.as_view()), name='product_list'),
    path('add-product',login_required(login_url='sign_in')(AddProduct.as_view()), name='add_product'),
    path('edit-product/<pk>',login_required(login_url='sign_in')(EditProduct.as_view()), name='edit_product'),
    path('delete-product/<pk>',login_required(login_url='sign_in')(DeleteProduct.as_view()), name='delete_product'),
    path('basket-list/<pk>',login_required(login_url='sign_in')(StoreBasketList.as_view()), name='basket_list'),
    path('basket-list/basket-update/<pk>',login_required(login_url='sign_in')(UpdateBasketStatus.as_view()), name='basket_update'),
    path('basket-detail/<pk>',login_required(login_url='sign_in')(BasketDetail.as_view()), name='basket_detail'),
    path('profile/<pk>',login_required(login_url='sign_in')(SellerProfile.as_view()), name='profile'),
    path('buyers-list',login_required(login_url='sign_in')(BuyersList.as_view()), name='buyers_list'),


    path('chart/<pk>',login_required(login_url='sign_in')(ChartView.as_view()), name='store_chart'),
    


]