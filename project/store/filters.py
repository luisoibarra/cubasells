import django_filters as dfil
from project.models import *
from django import forms

class StoreFilter(dfil.FilterSet):
    create_date_gte =dfil.DateFromToRangeFilter(
        field_name='Create_Date',lookup_expr='gte',widget=forms.SelectDateWidget(
            years=range(1959,2059)
            )
        )
    create_date_lte = dfil.DateFromToRangeFilter(
        field_name='Create_Date', lookup_expr='lte', widget=forms.SelectDateWidget(
            years=range(1959, 2059)
            )
        )
    class Meta:
        model = Store
        fields = {
            'Name':['icontains'],
            'Description':['icontains'],
        }
