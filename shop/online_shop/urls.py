from django.urls import path
from .views import *


urlpatterns = [
    path('',TemplateView.as_view(), name='dashboard'),
    path('profile',TemplateView4.as_view(), name= 'profile'),

    path('sign-in',SignInSeller.as_view(), name='sign_in'),
    path('sign-up',SignUpSeller.as_view() , name='sign_up'),
    path('store-list',SellerStoreList.as_view(), name='store_list'),
    path('create-store',CreateStore.as_view(), name='create_store'),
    path('delete-store/<pk>',DeleteStore.as_view(), name='delete_store'),
    path('edit-store/<pk>',EditStore.as_view(), name='edit_store'),
    path('add-product',AddProduct.as_view(), name='add_product'),
    path('basket-list/<pk>',StoreBasketList.as_view(), name='basket_list'),
    path('basket-detail/<pk>',BasketDetail.as_view(), name='basket_detail'),

    
    
    



]