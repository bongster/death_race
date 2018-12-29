from django import forms

# Register your models here.
from .models import Game, WOD, WOD2Game, Team2Game, Competition, Record, Game2Sponsor
from teams.models import Team
from sponsors.models import Sponsor


class CustomChoiceField(forms.ChoiceField):
    def label_from_instance(self, obj):
        return "%s %s" % (obj.id, obj.name)


class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s %s" % (obj.id, obj.name)


class WOD2GameForm(forms.ModelForm):
    wod_id = CustomModelChoiceField(
        queryset=WOD.objects.order_by('name'),
        empty_label=None,
    )
    game_id = CustomModelChoiceField(
        queryset=Game.objects.order_by('name'),
        empty_label=None,
    )

    def clean(self):
        if isinstance(self.cleaned_data.get('wod_id'), WOD):
            self.cleaned_data['wod_id'] = self.cleaned_data['wod_id'].id

        if isinstance(self.cleaned_data.get('game_id'), Game):
            self.cleaned_data['game_id'] = self.cleaned_data['game_id'].id

        return super().clean()

    class Meta:
        model = WOD2Game
        fields = '__all__'


class Team2GameForm(forms.ModelForm):
    team_id = CustomModelChoiceField(
        queryset=Team.objects.order_by('name'),
        empty_label=None,
    )
    game_id = CustomModelChoiceField(
        queryset=Game.objects.order_by('name'),
        empty_label=None,
    )

    def clean(self):
        if isinstance(self.cleaned_data.get('team_id'), Team):
            self.cleaned_data['team_id'] = self.cleaned_data['team_id'].id

        if isinstance(self.cleaned_data.get('game_id'), Game):
            self.cleaned_data['game_id'] = self.cleaned_data['game_id'].id

    class Meta:
        model = Team2Game
        fields = '__all__'


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


class CustomUIModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.name


class LeaderboardForm(forms.Form):
    search = forms.CharField(
        required=False,
        initial='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-2 mr-sm-2 mb-sm-0 bd-highlight'
            }
        )
    )

    division = forms.ChoiceField(
        required=False,
        choices=((None, 'Gender'),) + Team.GENTER_TYPE,
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

    competition = CustomUIModelChoiceField(
        required=False,
        queryset=Competition.objects.all(),
        empty_label='Competition',
        widget=forms.Select(
            attrs={
                'class': 'form-control mb-2 mr-sm-2 mb-sm-0 bd-highlight'
            }
        )
    )

    sort_key = CustomUIModelChoiceField(
        required=False, queryset=WOD.objects.all(),
        label='sort',
        empty_label='Sort',
        widget=forms.Select(
            attrs={
                'class': 'form-control mb-2 mr-sm-2 mb-sm-0 bd-highlight'
            }
        )
    )

    team_type = forms.ChoiceField(
        required=False,
        choices=((None, 'Type'),) + Team.TEAM_TYPE,
        widget=forms.Select(
            attrs={
                'class': 'form-control mb-2 mr-sm-2 mb-sm-0 bd-highlight'
            }
        )
    )


class CompetitionForm(forms.ModelForm):
    game_id = CustomModelChoiceField(
        queryset=Game.objects.order_by('name'),
        required=False,
    )

    def clean(self):
        if isinstance(self.cleaned_data.get('game_id'), Game):
            self.cleaned_data['game_id'] = self.cleaned_data['game_id'].id

        return super().clean()

    class Meta:
        model = Competition
        fields = '__all__'


class WODForm(forms.ModelForm):
    competition_id = CustomModelChoiceField(
        queryset=Competition.objects.order_by('name'),
        required=False,
    )

    def clean(self):
        if isinstance(self.cleaned_data.get('competition_id'), Competition):
            self.cleaned_data['competition_id'] = self.cleaned_data['competition_id'].id
        return super().clean()

    class Meta:
        model = WOD
        fields = '__all__'


class Game2SponsorForm(forms.ModelForm):
    game_id = CustomModelChoiceField(
        queryset=Game.objects.order_by('name'),
        empty_label=None,
    )
    sponsor_id = CustomModelChoiceField(
        queryset=Sponsor.objects.order_by('name'),
        empty_label=None,
    )

    def clean(self):
        if isinstance(self.cleaned_data.get('game_id'), Game):
            self.cleaned_data['game_id'] = self.cleaned_data['game_id'].id

        if isinstance(self.cleaned_data.get('sponsor_id'), Sponsor):
            self.cleaned_data['sponsor_id'] = self.cleaned_data['sponsor_id'].id

        return super().clean()

    class Meta:
        model = Game2Sponsor
        fields = '__all__'
