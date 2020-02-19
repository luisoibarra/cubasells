import django_filters as dfil
from project.models import *

class OfferFilter(dfil.FilterSet):
    class Meta:
        model = Offer
        fields = {
            'Price':['lte'],
            'Offer_name':['icontains'],
            'Store__Name':['icontains'],
        }

class StoreFilter(dfil.FilterSet):
    class Meta:
        model = Store
        fields = {
            'Name':['icontains'],
            'Create_Date':['lte'],
        }

class ProductFilter(dfil.FilterSet):
    class Meta:
        model = Product
        fields = {
            'Name':['icontains'],
            'Store_Amount':['lte'],
        }

class SubOfferFilter(dfil.FilterSet):
    class Meta:
        model = SubOffer
        fields = {
            'Product_offer__Name':['icontains'],
            'Amount':['lte'],
        }

class TagFilter(dfil.FilterSet):
    class Meta:
        model = Tag
        fields = {
            'Tag':['icontains'],
        }

class ImageFilter(dfil.FilterSet):
    class Meta:
        model = Image
        fields = {
            'Name':['icontains'],
        }