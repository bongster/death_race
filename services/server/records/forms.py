from django import forms
from commons.forms import CustomModelChoiceField

from .models import Record
from games.models import WOD
from teams.models import Team


class RecordForm(forms.ModelForm):
    team_id = CustomModelChoiceField(
        queryset=Team.objects.order_by('name'),
        empty_label=None,
    )
    wod_id = CustomModelChoiceField(
        queryset=WOD.objects.order_by('name'),
        empty_label=None,
    )

    def clean(self):
        if isinstance(self.cleaned_data.get('team_id'), Team):
            self.cleaned_data['team_id'] = self.cleaned_data['team_id'].id

        if isinstance(self.cleaned_data.get('wod_id'), WOD):
            self.cleaned_data['wod_id'] = self.cleaned_data['wod_id'].id

        return super().clean()

    class Meta:
        model = Record
        fields = '__all__'
