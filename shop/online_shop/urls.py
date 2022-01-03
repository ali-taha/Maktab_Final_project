from django.urls import path
from .views import *


urlpatterns = [
    path('',TemplateView.as_view(), name='dashboard'),
    path('sign-in',SignInSeller.as_view(), name='sign_in'),
    path('sign-up',SignUpSeller.as_view() , name='sign_up'),
    path('store_list',SellerStoreList.as_view(), name='store_list'),
    path('create_store',CreateStore.as_view(), name='create_store'),
    path('delete_store/<pk>',DeleteStore.as_view(), name='delete_store'),
    path('edit_store/<pk>',EditStore.as_view(), name='edit_store'),
    path('profile',TemplateView4.as_view(), name= 'profile'),


]