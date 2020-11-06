from django import forms
from project.models import Auction,BankAccount
from project.custom.forms import OrderForm
from django.core.exceptions import ValidationError
from django.utils import timezone

class AuctionCreateForm(forms.ModelForm):
    success_url = forms.CharField(widget=forms.HiddenInput(),required=False)

    class Meta:
        model = Auction
        exclude=['Winner','Password','Ended','Deposit','Status']
        
        field_classes = {
            'Initial_Date':forms.SplitDateTimeField,
            'Final_Date':forms.SplitDateTimeField,
        }
        
        widgets = {
            'Initial_Date':forms.SplitDateTimeWidget(date_attrs={'type':'date'},
                                                     time_attrs={'type':'time'}),
            'Final_Date':forms.SplitDateTimeWidget(date_attrs={'type':'date'},
                                                     time_attrs={'type':'time'}),
        }

    def clean_Initial_Date(self):
        if 'Initial_Date' in self.cleaned_data:
            data = self.cleaned_data["Initial_Date"]
            if data <= timezone.now():
                raise ValidationError('Initial Date must be a future date')
            return data
    
    def clean_Final_Date(self):
        if 'Final_Date' in self.cleaned_data and 'Initial_Date' in self.cleaned_data:
            data = self.cleaned_data["Final_Date"]
            data2 = self.cleaned_data["Initial_Date"]
            from datetime import timedelta
            diff = data - data2
            if diff < timedelta(minutes=5):
                raise ValidationError('The minimun auction duration is 5 minutes')
            return data
        return self.cleaned_data.get('Final_Date',None)
class AuctionPushForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    
    account = forms.ModelChoiceField(BankAccount.objects.all())
    
    money = forms.FloatField(min_value=0.01)

class AuctionOrderForm(OrderForm):
    model = Auction
    fields_to_order = ['Ended','Initial_Date','Money','Offered__Offer_name']
