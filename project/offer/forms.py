from django import forms
from project.models import Offer
from project.custom.forms import OrderForm
from django.core.exceptions import ValidationError
class OfferCreateForm(forms.ModelForm):
    
    class Meta:
        model = Offer
        exclude=['Store','buy_offer']

    def clean_Price(self):
        data = self.cleaned_data["Price"]
        if data <= 0:
            raise ValidationError('Price must be a positive number')
        return data
    
class OfferUserCreateForm(forms.ModelForm):
    
    class Meta:
        model = Offer
        exclude=['Store','buy_offer','Suboffer',]


class OfferOrderForm(OrderForm):
    model = Offer
    fields_to_order = ['Price','Offer_name','Store__name']
