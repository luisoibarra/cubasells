from django import forms
from project.models import *
from project.custom.forms import OrderForm

class TagCreateForm(forms.ModelForm):
    
    class Meta:
        model = Tag
        fields = '__all__'

class ImageCreateForm(forms.ModelForm):
    
    class Meta:
        model = Image
        fields = '__all__'



class TagOrderForm(OrderForm):
    model = Tag
    fields_to_order = ['Tag']

class ImageOrderForm(OrderForm):
    model = Image
    fields_to_order = ['Name']