from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from project.models import *

class MyUserCreateForm(UserCreationForm):
    
    class Meta:
        model = MyUser

        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'Phone',
            'Description',
            'Images',
            'Tags',
            'Accounts',
        ]

        labels = {
            'Username':'Username',
            'First_Name':'First_Name',
            'Last_Name':'Last_Name',
            'Email':'Email',
            'Phone':'Phone',
            'Description':'Description',
            'Images':'Images',
            'Tags':'Tags',
            'Accounts':'Accounts',
        }

        widgets = {
            'Username': forms.TextInput(attrs={'class':'form-control'}),
            'First_Name': forms.TextInput(attrs={'class':'form-control'}),
            'Last_Name': forms.TextInput(attrs={'class':'form-control'}),
            'Email': forms.EmailInput(attrs={'class':'form-control'}),
            'Phone':forms.NumberInput(attrs={'class':'form-control'}),
            'Description':forms.TextInput(attrs={'class':'form-control'}),
            'Images':forms.SelectMultiple(attrs={'class':'form-control'}),
            'Tags':forms.SelectMultiple(attrs={'class':'form-control'}),
            'Accounts':forms.SelectMultiple(attrs={'class':'form-control'}),
        }