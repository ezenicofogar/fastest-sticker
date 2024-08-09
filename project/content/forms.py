from django import forms
from .models import QueryGroup

class QueryGroupForm(forms.ModelForm):
    class Meta:
        model = QueryGroup
        fields = ['type']
    
class QueryGroupAddImageForm(forms.Form):
    image_pk = forms.IntegerField(required=True, label='ID')