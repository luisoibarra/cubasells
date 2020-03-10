from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from project.models import *
from project.custom.forms import OrderForm

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
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.Cart = ShoppingCart()
        user.Cart.save()
        user.Cart_id = user.Cart.id
        if commit:
            user.save()
            self.save_m2m()
        return user

class AuctionCreateForm(forms.ModelForm):
    auction_minim_time = 30 # In minutes
    auction_aticipation = 60 # In minutes
    class Meta:
        model = Auction
        exclude = ['winner',]
    
    def clean_duration(self):
        data = self.cleaned_data["duration"]
        data /= 60
        if data < self.auction_minim_time:
            raise ValidationError('The minimun time of an auction is %(minutes) minutes',code='invalid duration',params={'minutes':self.auction_minim_time})
        return data
    
    def clean_initial_date(self):
        data = self.cleaned_data["initial_date"]
        import datetime as dt
        if data < dt.datetime.now() + dt.datetime(minute=self.auction_aticipation):
            raise ValidationError('The initial date must have at least %(minutes) minutes of anticipation',code='invalid initial date',params={'minutes':self.auction_aticipation})
        return data

