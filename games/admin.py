from django.contrib import admin

# Register your models here.
from .models import Game, WOD, WOD2Game, Team, Team2Game, Record, Competition, Sponsor
from .forms import WOD2GameForm, Team2GameForm, RecordForm, WODForm, CompetitionForm, SponsorForm


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Game._meta.get_fields()] + [
        'logo_image_tag',
        'main_image_tag',
        'competition_list',
        'sponed_sponsor_list',
    ]


@admin.register(WOD)
class WODAdmin(admin.ModelAdmin):
    form = WODForm
    list_display = [field.name for field in WOD._meta.get_fields()]


@admin.register(WOD2Game)
class WOD2GameAdmin(admin.ModelAdmin):
    form = WOD2GameForm
    list_display = [field.name for field in WOD2Game._meta.get_fields()]


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Team._meta.get_fields()]


@admin.register(Team2Game)
class Team2GameAdmin(admin.ModelAdmin):
    form = Team2GameForm
    list_display = [field.name for field in Team2Game._meta.get_fields()]


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    form = RecordForm
    list_display = [field.name for field in Record._meta.get_fields()] + [
        'wod_name',
        'team_name',
    ]


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    form = CompetitionForm
    list_display = [field.name for field in Competition._meta.get_fields()] + [
        'game_name',
        'wod_list',
    ]


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    form = SponsorForm
    list_display = [field.name for field in Sponsor._meta.get_fields()] + [
        'participated_game_list',
    ]
