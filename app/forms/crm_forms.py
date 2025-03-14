from django import forms
from ..models import CRM

class PersonForm(forms.ModelForm):
    class Meta:
        model = CRM
        fields = ['hostname', 'mail', 'vendor']