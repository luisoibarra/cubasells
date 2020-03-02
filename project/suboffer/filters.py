import django_filters as dfil
from project.models import *


class SubOfferFilter(dfil.FilterSet):
    class Meta:
        model = SubOffer
        fields = {
            'Product_offer__Name':['icontains'],
            'Amount':['lte'],
        }
