from django import forms
from project.models import Chat,MyUser
from project.custom.forms import OrderForm
from django.core.exceptions import ObjectDoesNotExist,ValidationError


class ChatCreateForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['Message']
        cols = 25
        
        widgets = {
            'Message':forms.Textarea(attrs={'required':"", 'rows':1,'cols':cols, 'class': 'message-form'})
        }

    def clean_Message(self):
        if "Message" in self.cleaned_data:
            data = self.cleaned_data["Message"]
            new_data = ''
            for y in [(x if i%self.Meta.cols else x+'\n') for i,x in enumerate(data,1)]:
                new_data += y
            return new_data
    
class UserSearchForm(forms.Form):
    username = forms.CharField(required ="")
    
    def clean_username(self):
        data = self.cleaned_data["username"]
        try:
            user = MyUser.objects.get(username=data)
        except ObjectDoesNotExist:
            raise ValidationError(f' {data} no exist')
        data = self.cleaned_data['username'] = user.id
        return data
    

class ChatOrderForm(OrderForm):
    model = Chat
    exclude = [
        'sender_user',
        'receiver_user',
        'Date',
        'Message',
        'type',
        ]
