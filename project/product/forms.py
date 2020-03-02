from django import forms
from project.models import *
from project.custom.forms import OrderForm

class ProductCreateForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ['Store']

class ProductOrderForm(OrderForm):
    model = Product
    fields_to_order = ['Store_Amount','Name']
