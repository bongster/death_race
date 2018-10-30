from django import forms

# Register your models here.
from .models import Game, WOD, WOD2Game, Team, Team2Game, Competition, Record, Sponsor, Game2Sponsor


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
        'class': 'form-control mb-2 mr-sm-2 mb-sm-0 bd-highlight'
    }))

    division = forms.ChoiceField(required=False, choices=((None, 'Gender'),) + Team.GENTER_TYPE,
                                 widget=forms.Select(attrs={
                                     'class': 'form-control mb-2 mr-sm-2 mb-sm-0 bd-highlight'
                                 }))

    def __init__(self, game_id, *args, **kwargs):
        super(LeaderboardForm, self).__init__(*args, **kwargs)
        self.fields['sort_key'].queryset = WOD.objects.filter(
            id__in=WOD.objects.filter(
                competition_id__in=Competition.objects.filter(
                    game_id=game_id,
                    is_active=True
                ).values_list('id', flat=True),
                is_active=True,
            )
        )

    competition = CustomModelChoiceField(required=False, queryset=Competition.objects.all(), empty_label='Competition',
                                         widget=forms.Select(attrs={
                                             'class': 'form-control mb-2 mr-sm-2 mb-sm-0 bd-highlight'
                                         }))

    sort_key = CustomModelChoiceField(required=False, queryset=WOD.objects.all(), label='sort', empty_label='Sort',
                                      widget=forms.Select(attrs={
                                          'class': 'form-control mb-2 mr-sm-2 mb-sm-0 bd-highlight'
                                      }))

    team_type = forms.ChoiceField(required=False, choices=((None, 'Type'),) + Team.TEAM_TYPE,
                                  widget=forms.Select(attrs={
                                      'class': 'form-control mb-2 mr-sm-2 mb-sm-0 bd-highlight'
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


class SponsorForm(forms.ModelForm):
    class Meta:
        model = Sponsor
        fields = '__all__'


class Game2SponsorForm(forms.ModelForm):
    game_id = CustomChoiceField(choices=Game.objects.all().values_list('id', 'name'))
    sponsor_id = CustomChoiceField(choices=Sponsor.objects.all().values_list('id', 'name'))

    class Meta:
        model = Game2Sponsor
        fields = '__all__'
