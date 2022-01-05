import django_filters
from .models import Basket

class BasketListFilter(django_filters.FilterSet):
    class Meta:
        model = Basket
        fields = {
            'status': ['exact'],
        }