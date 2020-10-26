import django_filters as dfil
from project.models import *

class OfferFilter(dfil.FilterSet):
    class Meta:
        model = Offer
        fields = {
            'Price':['gte','lte'],
            'Offer_name':['icontains'],
            'Store__Name':['icontains'],
        }


