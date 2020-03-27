import django_filters as dfil
from project.models import Auction

class AuctionFilter(dfil.FilterSet):
    class Meta:
        model = Auction
        fields = {
            'Money':['lte'],
            'Offered__Offer_name':['icontains'],
            'Initial_Date':['lte'],
            # 'Ended':['icontains'],
            
        }

