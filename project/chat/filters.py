import django_filters as dfil
from project.models import *
from django import forms
import datetime
class ChatFilter(dfil.FilterSet):
    year = datetime.date.today().year
    Date = dfil.DateRangeFilter(widget=forms.SelectDateWidget(years=range(2015,year)))
    type = dfil.CharFilter('type',widget=dfil.widgets.forms.widgets.Select(choices=(('','--------'),('I','Important'),('W','Warning'),('N','Normal'))))
    class Meta:
        model = Chat
        fields = [
            'Date',
            'type'
            ]
