from django.urls import path
from online_shop.views import StoreListApi, StoreTypeListApi, ProductListApi, BasketCreateApi, AddBasketItemApi, DeleteBasketItemApi, PayBasketApi, PaidBasketsApi



urlpatterns = [

    path('store/list',StoreListApi.as_view(), name='store_list_api'),
    path('store/type',StoreTypeListApi.as_view(), name='store_type_list_api'),
    path('<int:store>/product',ProductListApi.as_view(), name='product_list_api'),
    path('basket/product/<int:product>',BasketCreateApi.as_view(), name='basket_create_api'),
    path('basket/<int:basket_id>/product/<int:product_id>/basket-item/',AddBasketItemApi.as_view(), name='basket_add_item_api'),
    path('basket-item/<int:id>',DeleteBasketItemApi.as_view(), name='delete_basket_item_api'),
    path('basket2/<int:id>',PayBasketApi.as_view(), name='pay_basket_api'),
    path('basket3/',PaidBasketsApi.as_view(), name='paid_baskets_api'),

]
