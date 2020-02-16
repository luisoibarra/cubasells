from django import forms

class OrderForm(forms.Form):
    
    model = None
    fields_to_order = None
    exclude = None
    
    def __init__(self, *args, **kwargs):
        field_dict = forms.fields_for_model(self.model)
        self.fields_name = [x for x in field_dict]
        
        if self.exclude:
            for x in self.fields_name:
                if not x in self.exclude:
                    setattr(self,x,forms.BooleanField(required=False,label=field_dict[x].label,help_text=f'Order by  {field_dict[x].label}'))
                    setattr(self,f'{x}_decrease',forms.BooleanField(required=False,label=f'{field_dict[x].label} decrease',help_text=f'Order by {field_dict[x].label} decreasingly'))
        elif self.fields_to_order:
            for x in self.fields_to_order:
                key = [y for y in field_dict if x.startswith(y)][0]
                label = field_dict[key].label
                setattr(self,x,forms.BooleanField(required=False,label=label,help_text=f'Order by  {label}'))
                setattr(self,f'{x}_decrease',forms.BooleanField(required=False,label=f'{label} decrease',help_text=f'Order by {label} decreasingly'))
        else:
            for x in self.fields_name:
                setattr(self,x,forms.BooleanField(required=False,label=field_dict[x].label,help_text=f'Order by  {field_dict[x].label}'))
                setattr(self,f'{x}_decrease',forms.BooleanField(required=False,label=f'{field_dict[x].label} decrease',help_text=f'Order by {field_dict[x].label} decreasingly'))
            
        super(forms.Form, self).__init__(*args, **kwargs)
        
        if self.exclude:
            for x in self.fields_name:
                if not x in self.exclude:
                    self.fields[x] = forms.BooleanField(required=False,label=field_dict[x].label,help_text=f'Order by  {field_dict[x].label}')
                    self.fields[f'{x}_decrease'] = forms.BooleanField(required=False,label=f'{field_dict[x].label} decrease',help_text=f'Order by {field_dict[x].label} decreasingly')

        elif self.fields_to_order:
            for x in self.fields_to_order:
                key = [y for y in field_dict if x.startswith(y)][0]
                label = field_dict[key].label
                self.fields[x] = forms.BooleanField(required=False,label=label,help_text=f'Order by  {label}')
                self.fields[f'{x}_decrease'] = forms.BooleanField(required=False,label=f'{label} decrease',help_text=f'Order by {label} decreasingly')

        else:
            for x in self.fields_name:
                self.fields[x] = forms.BooleanField(required=False,label=field_dict[x].label,help_text=f'Order by  {field_dict[x].label}')
                self.fields[f'{x}_decrease'] = forms.BooleanField(required=False,label=f'{field_dict[x].label} decrease',help_text=f'Order by {field_dict[x].label} decreasingly')
