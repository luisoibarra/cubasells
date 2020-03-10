import django_filters as dfil
from project.models import *


class ShoppingOfferFilter(dfil.FilterSet):
    class Meta:
        model = ShoppingOffer
        fields = {
            'Offer__Price':['lte'],
            'Offer__Offer_name':['icontains'],
            'Offer__Store__Name':['icontains'],
        }

