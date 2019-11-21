from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from project.models import *

class UserCreateForm(UserCreationForm):
    
    first_name =  forms.CharField(max_length=50,required=False)
    
    last_name =  forms.CharField(max_length=50,required=False)
    
    email = forms.EmailField(required=True)
    
    def save(self,commit=True):
        instance = super().save(commit)
        instance.first_name = self.cleaned_data['first_name']
        instance.last_name = self.cleaned_data['last_name']
        instance.email = self.cleaned_data['email']
        if commit:
            instance.save()
        return instance

class MyUserCreateForm(forms.ModelForm):
    
    class Meta:
        model = MyUser

        fields = [
            'Phone',
            'Description',
            'Images',
            'Tags',
            'Accounts',
        ]

        labels = {
            'Phone':'Phone',
            'Description':'Description',
            'Images':'Images',
            'Tags':'Tags',
            'Accounts':'Accounts',
        }

        widgets = {
            'Phone':forms.NumberInput(attrs={'class':'form-control'}),
            'Description':forms.TextInput(attrs={'class':'form-control'}),
            'Images':forms.SelectMultiple(attrs={'class':'form-control'}),
            'Tags':forms.SelectMultiple(attrs={'class':'form-control'}),
            'Accounts':forms.SelectMultiple(attrs={'class':'form-control'}),
        }