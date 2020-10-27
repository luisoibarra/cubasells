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
        exclude = ['Owner']

class MultiSelectSTagForm(forms.Form):

    def __init__(self, tags, *args, **kwargs):
        if tags is None:
            tags = []
        setattr(self, 'tags', forms.ChoiceField(
            choices=[(x.id, x.Tag) for x in tags]))
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['tags'] = self.tags

class MultiSelectTagForm(forms.Form):
    def __init__(self, tags, *args, **kwargs):
        if tags is None:
            tags = []
        setattr(self, 'tags', forms.MultipleChoiceField(
            choices=[(x.id, x.Tag) for x in tags],required=False))
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['tags'] = self.tags

class TagNameForm(forms.Form):
    name = forms.CharField(label='Tag contains',required=False)

class TagOrderForm(OrderForm):
    model = Tag
    fields_to_order = ['Tag']

class ImageOrderForm(OrderForm):
    model = Image
    fields_to_order = ['Name']