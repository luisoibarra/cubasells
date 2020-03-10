from django import forms
from project.models import *
from project.custom.forms import OrderForm


class ShoppingOfferOrderForm(OrderForm):
    model = ShoppingOffer
    fields_to_order = ['Offer__Price','Offer__Offer_name','Offer__Store__Name','Amount']

class ShoppingOfferCreateForm(forms.ModelForm):
    
    class Meta:
        model = ShoppingOffer
        fields = ["Amount",]
