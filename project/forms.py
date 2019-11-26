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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            self.save_m2m()
        return user

class StoreCreateForm(forms.ModelForm):
    
    class Meta:
        model = Store
        exclude=['Owner',]

class ProductCreateForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ['Store']

class OfferCreateForm(forms.ModelForm):
    
    class Meta:
        model = Offer
        exclude=['Store','buy_offer']

class SubOfferCreateForm(forms.ModelForm):
    
    class Meta:
        model = SubOffer
        fields = '__all__'