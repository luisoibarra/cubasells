import django_filters as dfil
from project.models import *


class ProductFilter(dfil.FilterSet):
    class Meta:
        model = Product
        fields = {
            'Name':['icontains'],
            'Store_Amount':['lte'],
        }
