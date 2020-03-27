from django import forms
from project.models import Auction,BankAccount
from project.custom.forms import OrderForm
from django.core.exceptions import ValidationError
from django.utils import timezone

class AuctionCreateForm(forms.ModelForm):
    
    class Meta:
        model = Auction
        exclude=['Winner','Password','Ended','Deposit']

    def clean_Initial_Date(self):
        data = self.cleaned_data["Initial_Date"]
        if data <= timezone.now():
            raise ValidationError('Initial Date must be a future date')
        return data
    
    def clean_Final_Date(self):
        data = self.cleaned_data["Final_Date"]
        data2 = self.cleaned_data["Initial_Date"]
        from datetime import timedelta
        diff = data - data2
        if diff < timedelta(minutes=5):
            raise ValidationError('The minimun auction duration is 5 minutes')
        return data

class AuctionPushForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    
    account = forms.ModelChoiceField(BankAccount.objects.all())
    
    money = forms.FloatField(min_value=0.01)

class AuctionOrderForm(OrderForm):
    model = Auction
    fields_to_order = ['Ended','Initial_Date','Money','Offered__Offer_name']
