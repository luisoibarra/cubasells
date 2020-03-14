from django import forms
from project.models import BankAccount
from project.custom.forms import OrderForm

class BankAccountCreateForm(forms.ModelForm):
    
    class Meta:
        model = BankAccount
        fields = ['Account',]


class BankAccountOrderForm(OrderForm):
    model = BankAccount
    fields_to_order = ['Account',]
