import django_filters as dfil
from project.models import *

class ChatFilter(dfil.FilterSet):
    Date = dfil.DateRangeFilter()
    type = dfil.CharFilter('type',widget=dfil.widgets.forms.widgets.Select(choices=(('','--------'),('I','Important'),('W','Warning'),('N','Normal'))))
    class Meta:
        model = Chat
        fields = [
            'Date',
            'type'
            ]

class ChatUserFilter(dfil.FilterSet):
    class Meta:
        model = User
        fields = {
            'username':['icontains'],
        }
