from django.urls import path
from .views import *


urlpatterns = [
    path('',TemplateView.as_view(), name='dashboard'),
    path('sign-in',SignInSeller.as_view(), name='sign-in'),
    path('sign-up',SignUpSeller.as_view() , name='sign-up'),
    path('profile',TemplateView4.as_view(), name= 'profile'),
    path('store_detail',SellerStoreList.as_view(), name='store_detail'),
    path('create_store',CreateStore.as_view(), name='create_store'),
    path('delete_store/<pk>',DeleteStore.as_view(), name='delete_store'),

]