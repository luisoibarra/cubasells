from django import forms
from project.models import BankAccount
from project.custom.forms import OrderForm
from project.bank.models import BankAccount as TrueBankAccount
from django.forms import ValidationError

class BankAccountCreateForm(forms.ModelForm):
    
    class Meta:
        model = BankAccount
        fields = ['Account',]
        
    def clean_Account(self):
        if 'Account' in self.cleaned_data:
            data = self.cleaned_data["Account"]
            qs = TrueBankAccount.objects.filter(Number=data)
            if len(qs) == 0:
                raise ValidationError('The number account dont exist in the bank, please check the number or create the account')
            return data
        
    


class BankAccountOrderForm(OrderForm):
    model = BankAccount
    fields_to_order = ['Account',]
