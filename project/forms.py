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
            # 'Images'
        ]

        widgets = {
        'username': forms.TextInput(attrs={'class':'form-control' ,'placeholder':'Username'}),
        'first_name': forms.TextInput(attrs={'class':'form-control','placeholder':'Name'}),
        'last_name': forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
        'email' : forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}),
        'Phone' : forms.TextInput(attrs={'class':'form-control','placeholder':'Phone'}),
        'Description': forms.TextInput(attrs={'class':'form-control','placeholder':'Description'}),
        # 'Images': forms.FileInput(attrs={'class':'form-group','placeholder':'Add Image'}),
        # 'Accounts': forms.Select(),
        #'password': forms.TextInput(attrs= {'class':'form-control','placeholder':'Password'}),
        #'password1' : forms.TextInput(attrs= {'class':'form-control','placeholder':'Confirm Password'}),
    }

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

class MyUserUpdateForm(UserCreationForm):
    
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
    auction_anticipation = 60 # In minutes
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
        if data < dt.datetime.now() + dt.datetime(minute=self.auction_anticipation):
            raise ValidationError('The initial date must have at least %(minutes) minutes of anticipation',code='invalid initial date',params={'minutes':self.auction_anticipation})
        return data

class DeleteSuccessURLForm(forms.Form):
    success_url = forms.CharField(widget=forms.HiddenInput())
    