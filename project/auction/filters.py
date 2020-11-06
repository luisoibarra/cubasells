import django_filters as dfil
from project.models import Auction
from django import forms
import datetime

class AuctionFilter(dfil.FilterSet):
    year = datetime.date.today().year+50
    Initial_Date = dfil.DateTimeFilter(
        field_name='Initial_Date',lookup_expr='lte',widget=forms.SelectDateWidget(
            years=range(2019,year+1)
            )
        )
    class Meta:
        model = Auction
        fields = {
            'Money':['lte'],
            'Offered__Offer_name':['icontains'],
            # 'Initial_Date':['lte'],
            # 'Ended':['icontains'],
        }

