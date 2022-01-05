from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *


urlpatterns = [

    path('',login_required(SellerStoreList.as_view()), name='store_list'),
    path('create-store',login_required(CreateStore.as_view()), name='create_store'),
    path('delete-store/<pk>',login_required(DeleteStore.as_view()), name='delete_store'),
    path('edit-store/<pk>',login_required(EditStore.as_view()), name='edit_store'),
    path('product-list',login_required(SellerProductList.as_view()), name='product_list'),
    path('add-product',login_required(AddProduct.as_view()), name='add_product'),
    path('edit-product/<pk>',login_required(EditProduct.as_view()), name='edit_product'),
    path('delete-product/<pk>',login_required(DeleteProduct.as_view()), name='delete_product'),
    path('basket-list/<pk>',login_required(StoreBasketList.as_view()), name='basket_list'),
    path('basket-list/basket-update/<pk>',login_required(UpdateBasketStatus.as_view()), name='basket_update'),
    path('basket-detail/<pk>',login_required(BasketDetail.as_view()), name='basket_detail'),
    path('profile/<pk>',login_required(SellerProfile.as_view()), name='profile'),

    path('chart/<pk>',login_required(ChartView.as_view()), name='store_chart'),
    


]