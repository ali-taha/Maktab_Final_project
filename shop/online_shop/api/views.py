from django.contrib.auth import  get_user_model
from online_shop.models import Store, Product, Basket, BasketItem, StoreType
from django.http import Http404
from django.db.models import Q, Avg, Count, Sum
from rest_framework import status, generics, mixins, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from online_shop.api.serializers import StoreListSerializer, StoreTypeListSerializer, ProductListSerializer, CreateBasketSerializer, CreateBasketItemSerializer, DeleteBasketItemSerializer, PayBasketerializer, ShowBasketsSerializer
from online_shop.filter import StoreListFilter, StoreTypeFilter,ProductListFilter


User = get_user_model()

class StoreListApi(generics.ListAPIView):
    filterset_class = StoreListFilter
    permission_classes = (IsAuthenticated,)
    serializer_class = StoreListSerializer

    def get_queryset(self):
        if self.request.method == "GET":
            return Store.alive.filter(status='con')


class StoreTypeListApi(generics.ListAPIView):
    filterset_class = StoreTypeFilter
    permission_classes = (IsAuthenticated,)
    serializer_class = StoreTypeListSerializer

    def get_queryset(self):
        if self.request.method == "GET":
            return StoreType.objects.all()    


class ProductListApi(generics.ListAPIView):
    filterset_class = ProductListFilter
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductListSerializer

    def get_queryset(self):
        if self.request.method == "GET":
            return Product.available.filter(store__id=self.kwargs.get('store'))     


class BasketCreateApi(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset =Product.objects.all()
    serializer_class = CreateBasketSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id  = self.kwargs.get('product')
        product = Product.objects.get(id=product_id)
        store = product.store 
        basket = self.perform_create(serializer, product, store)
        headers = self.get_success_headers(serializer.data)
        return Response(
            data={"basket_id": f"{basket.id}"},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )               

    def perform_create(self, serializer, product, store):
        basket  = serializer.save(owner=self.request.user,store=store)
        BasketItem.objects.create(basket=basket,product=product,count=1)
        return serializer.save(owner=self.request.user,store=store)  


class AddBasketItemApi(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset =BasketItem.objects.all()
    serializer_class = CreateBasketItemSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
  
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # basket = serializer.validated_data['basket']
        # product = serializer.validated_data['product']
        basket = Basket.objects.get(id=self.kwargs.get('basket_id'))
        product = Product.objects.get(id=self.kwargs.get('product_id')) 
        if basket.store == product.store:
            basket_item = self.perform_create(serializer, basket, product)
            headers = self.get_success_headers(serializer.data)
            return Response(
                    data={"Basket Item Successfully added": f"{basket_item.id}"},
                    status=status.HTTP_201_CREATED,
                    headers=headers,
                )
        else:
            return Response(
                data={"msg": " You Can't By From Some Stores in a Basket "},
                status=status.HTTP_403_FORBIDDEN,
            )

    def perform_create(self, serializer, basket, product):
        return serializer.save(basket=basket, product=product)   

class DeleteBasketItemApi(generics.DestroyAPIView):

    permission_classes = (IsAuthenticated,)
    queryset =BasketItem.objects.all()
    serializer_class = DeleteBasketItemSerializer

    lookup_field = "id"
    lookup_field_kwargs ="id"

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data={"msg": " Basket Deleted "},status=status.HTTP_200_OK)

class PayBasketApi(generics.UpdateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = PayBasketerializer

    lookup_field = "id"
    lookup_field_kwargs ="id"
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        # serializer.validated_data['status'] ='pai'
        serializer.save(status='pai')    
 
    def get_queryset(self):
        if self.request.method == "PUT":
            return Basket.objects.filter(owner=self.request.user)       

class ShowBasketsApi(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ShowBasketsSerializer

    def get_queryset(self):
          # for swagger warning
          if getattr(self, "swagger_fake_view", False):
              return Basket.objects.none() 
          elif self.kwargs.get('status') in ['rev','pai'] :
              return Basket.objects.filter(Q(owner=self.request.user)&Q(status=f"{self.kwargs.get('status')}"))
