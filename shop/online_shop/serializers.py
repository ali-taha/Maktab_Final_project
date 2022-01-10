from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Store, StoreType

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

 