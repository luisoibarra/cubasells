import django_filters as dfil
from project.models import *

class StoreFilter(dfil.FilterSet):
    class Meta:
        model = Store
        fields = {
            'Name':['icontains'],
            'Create_Date':['lte'],
        }
