from django import forms

from commons.models import Resource


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = '__all__'