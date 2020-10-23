from django import forms
from project.models import Store
from project.custom.forms import OrderForm

class MultiSelectSubOfferForm(forms.Form):

    def __init__(self, products,suboffers,*args, **kwargs):
        if products is None:
            products = []
        if suboffers is None:
            suboffers = []   
        setattr(self,'products',forms.ChoiceField(choices=[(x.id,x.Name) for x in products]))         
        setattr(self,'suboffers',forms.MultipleChoiceField(\
            choices=[((x.id,amount),x.Product_offer.Name + ' ' + str(amount)) for x,amount in suboffers]))         
        setattr(self,'amount',forms.IntegerField(min_value=1))         
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['products'] = self.products
        self.fields['suboffers'] = self.suboffers
        self.fields['amount'] = self.amount


class StoreCreateForm(forms.ModelForm):
    success_url = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = Store
        exclude=['Owner',]


class StoreOrderForm(OrderForm):
    model = Store
    fields_to_order = ['Name']
