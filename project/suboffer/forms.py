from django import forms
from project.models import SubOffer
from project.custom.forms import OrderForm

class SubOfferCreateForm(forms.ModelForm):
    
    class Meta:
        model = SubOffer
        fields = '__all__'

  
class SubOfferOrderForm(OrderForm):
    model = SubOffer
    fields_to_order = ['Product_offer__Name','Amount']

class SubOfferSelectForm(forms.Form):
    
    def __init__(self, queryset,*args, **kwargs):
        if not queryset is None:
            setattr(self,'suboffers',forms.ModelMultipleChoiceField(queryset,required=False))
        else:
            setattr(self,'suboffers',forms.ModelMultipleChoiceField(SubOffer.objects.none(),required=False))
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['suboffers'] = self.suboffers
    