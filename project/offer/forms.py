from django import forms
from project.models import Offer
from project.custom.forms import OrderForm

class OfferCreateForm(forms.ModelForm):
    
    class Meta:
        model = Offer
        exclude=['Store','buy_offer']


class OfferOrderForm(OrderForm):
    model = Offer
    fields_to_order = ['Price','Offer_name','Store__name']
