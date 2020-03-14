import django_filters as dfil
from project.models import *

class BankAccountFilter(dfil.FilterSet):
    class Meta:
        model = BankAccount
        fields = {
            'Account':['lte'],
        }


