from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Store, StoreType, Product, Basket, BasketItem

User = get_user_model()


class StoreListSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source="type.title", read_only=True)
    owner_name = serializers.CharField(source="owner.username", read_only=True)
#     type = serializers.SlugRelatedField(
#       slug_field = 'slug',queryset = StoreType.objects.all()
#    )

    class Meta:
        model = Store
        fields = ['title','type','type_name','owner','owner_name','status','description']
        lookup_field = 'title'

class StoreTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreType
        fields = "__all__"   

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"    

class CreateBasketSerializer(serializers.ModelSerializer):
    class Meta:
        model= Basket
        fields = []

class CreateBasketItemSerializer(serializers.ModelSerializer):
    class Meta:
        model= BasketItem
        fields = ['count'] 

class DeleteBasketItemSerializer(serializers.ModelSerializer):
    class Meta:
        model= BasketItem
        fields = ['id']   

class PayBasketerializer(serializers.ModelSerializer):
    class Meta:
        model= Basket
        fields = ['status']  


class PaidBasketsSerializer(serializers.ModelSerializer):
    class Meta:
        model= Basket
        fields = "__all__"                     


 