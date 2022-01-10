import django_filters
from .models import Basket, Store, StoreType

class BasketListFilter(django_filters.FilterSet):

    class Meta:
        model = Basket
        fields = {
            'status':['exact'],
            'created_on':['date__gt','date__lt'],
        }



class StoreListFilter(django_filters.FilterSet):
    class Meta:
        model = Store
        fields = {
            'type':['exact',],

        }   

        
           
          