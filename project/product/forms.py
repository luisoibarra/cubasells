from django import forms
from project.models import *
from project.custom.forms import OrderForm

class ProductCreateForm(forms.ModelForm):

    class Meta:
        model = Product
        #exclude = [Store]
        fields  = [
                'Name',
                'Store_Amount',
                'Description',
                'Tags',
                'Images',
        ]
        widgets = {
            'Name': forms.TextInput(attrs={'class':'form-group','placeholder':'Name'}),
            'Store_Amount': forms.TextInput(attrs={'class':'form-group','placeholder':'Store Amount'}),
            'Tags': forms.Select(attrs={'multiple':'true'}) ,
            'Description': forms.TextInput(attrs={'class':'form-group','placeholder':'Description'}),
            # 'Images': forms.FileInput(attrs={'class':'form-group','placeholder':'Add Image'}),
        }

class ProductOrderForm(OrderForm):
    model = Product
    fields_to_order = ['Store_Amount','Name']
