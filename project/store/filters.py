import django_filters as dfil
from project.models import *
from django import forms
import datetime

class StoreFilter(dfil.FilterSet):
    year = datetime.date.today().year
    create_date_gte =dfil.DateFromToRangeFilter(
        field_name='Create_Date',lookup_expr='gte',widget=forms.SelectDateWidget(
            years=range(2019,year)
            )
        )
    create_date_lte = dfil.DateFromToRangeFilter(
        field_name='Create_Date', lookup_expr='lte', widget=forms.SelectDateWidget(
            years=range(2019, year)
            )
        )
    class Meta:
        model = Store
        fields = {
            'Name':['icontains'],
            'Description':['icontains'],
        }
