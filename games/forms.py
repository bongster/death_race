from django import forms

# Register your models here.
from .models import Game, WOD, WOD2Game, Team, Team2Game, Record


class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return "%s %s" % (obj.id, obj.name)

class WOD2GameForm(forms.ModelForm):
    wod_id = CustomModelChoiceField(queryset=WOD.objects.all())
    game_id = CustomModelChoiceField(queryset=Game.objects.all())

    class Meta:
        model = WOD2Game
        fields = '__all__'

class Team2GameForm(forms.ModelForm):
    team_id = CustomModelChoiceField(queryset=Team.objects.all())
    game_id = CustomModelChoiceField(queryset=Game.objects.all())

    class Meta:
        model = Team2Game
        fields = '__all__'

class RecordForm(forms.ModelForm):
    team_id = CustomModelChoiceField(queryset=Team.objects.all())
    wod_id = CustomModelChoiceField(queryset=WOD.objects.all())

    class Meta:
        model = Record
        fields = '__all__'
