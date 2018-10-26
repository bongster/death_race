from django import forms

# Register your models here.
from .models import Game, WOD, WOD2Game, Team, Team2Game, Competition, Record


class CustomChoiceField(forms.ChoiceField):
    def label_from_instance(self, obj):
        return "%s %s" % (obj.id, obj.name)


class WOD2GameForm(forms.ModelForm):
    wod_id = CustomChoiceField(choices=WOD.objects.all().values_list('id', 'name'))
    game_id = CustomChoiceField(choices=Game.objects.all().values_list('id', 'name'))

    class Meta:
        model = WOD2Game
        fields = '__all__'


class Team2GameForm(forms.ModelForm):
    team_id = CustomChoiceField(choices=Team.objects.all().values_list('id', 'name'))
    game_id = CustomChoiceField(choices=Game.objects.all().values_list('id', 'name'))

    class Meta:
        model = Team2Game
        fields = '__all__'


class RecordForm(forms.ModelForm):
    team_id = CustomChoiceField(choices=Team.objects.all().values_list('id', 'name'))
    wod_id = CustomChoiceField(choices=WOD.objects.all().values_list('id', 'name'))

    class Meta:
        model = Record
        fields = '__all__'


class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.name


class WODModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.name


class LeaderboardForm(forms.Form):
    search = forms.CharField(required=False, initial='', widget=forms.TextInput(attrs={
        'class': 'form-control form-control-sm mr-sm-2'
    }))

    division = forms.ChoiceField(required=False, choices=((None, 'All'),) + Team.GENTER_TYPE,
                                 widget=forms.Select(attrs={
                                     'class': 'form-control form-control-sm mr-sm-2'
                                 }))

    def __init__(self, game_id, *args, **kwargs):
        super(LeaderboardForm, self).__init__(*args, **kwargs)
        self.fields['wod'].queryset = WOD.objects.filter(
            id__in=WOD2Game.objects.filter(
                game_id=game_id
            )
        )

    competition = CustomModelChoiceField(required=False, queryset=Competition.objects.all(), empty_label='All',
                                         widget=forms.Select(attrs={
                                             'class': 'form-control form-control-sm mr-sm-2'
                                         }))

    wod = CustomModelChoiceField(required=False, queryset=WOD.objects.all(), label='sort', empty_label='All',
                                 widget=forms.Select(attrs={
                                     'class': 'form-control form-control-sm mr-sm-2'
                                 }))


class CompetitionForm(forms.ModelForm):
    game_id = CustomChoiceField(
        choices=Game.objects.all().values_list('id', 'name')
    )

    class Meta:
        model = Competition
        fields = '__all__'


class WODForm(forms.ModelForm):
    competition_id = CustomChoiceField(
        choices=Competition.objects.all().values_list('id', 'name'),
    )

    class Meta:
        model = WOD
        fields = '__all__'