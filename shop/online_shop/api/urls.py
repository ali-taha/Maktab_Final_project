from django.urls import path
from online_shop.api.views import StoreListApi, StoreTypeListApi, ProductListApi, BasketCreateApi, AddBasketItemApi, DeleteBasketItemApi, PayBasketApi, ShowBasketsApi



urlpatterns = [

    path('store/list',StoreListApi.as_view(), name='store_list_api'),
    path('store/type',StoreTypeListApi.as_view(), name='store_type_list_api'),
    path('store/<int:store>/product',ProductListApi.as_view(), name='product_list_api'),
    path('basket/product/<int:product>',BasketCreateApi.as_view(), name='basket_create_api'),
    path('basket/<int:basket_id>/product/<int:product_id>/basket-item/',AddBasketItemApi.as_view(), name='basket_add_item_api'),
    path('basket-item/<int:id>',DeleteBasketItemApi.as_view(), name='delete_basket_item_api'),
    path('pay-basket/<int:id>',PayBasketApi.as_view(), name='pay_basket_api'),
    path('show-basket/<status>',ShowBasketsApi.as_view(), name='show_baskets_api'),

]
