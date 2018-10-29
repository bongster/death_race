from django import forms

from commons.models import Resource


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = '__all__'