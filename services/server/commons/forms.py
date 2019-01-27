from django import forms

from commons.models import Resource

class CustomChoiceField(forms.ChoiceField):
    def label_from_instance(self, obj):
        return "%s %s" % (obj.id, obj.name)


class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s %s" % (obj.id, obj.name)


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = '__all__'