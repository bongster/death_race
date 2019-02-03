import csv
import io

from django.contrib import admin

# Register your models here.
from django.shortcuts import redirect, render
from django.urls import path

from commons.forms import CsvImportForm
from commons.utils import ExportCsvMixin
from death_race.utils import get_or_none
from .models import Game, WOD, WOD2Game, Team2Game, Competition, Game2Sponsor
from teams.models import Team
from commons.models import Resource
from .forms import WOD2GameForm, Team2GameForm, WODForm, CompetitionForm, Game2SponsorForm
from sponsors.models import Sponsor


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'description',
        'start_date',
        'end_date',
        'logo_image_tag',
        'resources',
        'competition_list',
        'sponed_sponsor_list',
    ]


@admin.register(WOD)
class WODAdmin(admin.ModelAdmin):
    form = WODForm
    list_display = [field.name for field in WOD._meta.get_fields()] + [
        'competition_name',
    ]


@admin.register(Team2Game)
class Team2GameAdmin(admin.ModelAdmin):
    form = Team2GameForm
    list_display = [
        'id',
        'team_name',
        'game_name',
        'created_at',
        'updated_at',
        'is_active',
    ]

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    form = CompetitionForm
    list_display = [
        'id',
        'name',
        'game_name',
        'wod_list',
        'created_at',
        'updated_at',
        'is_active',
    ]


@admin.register(Game2Sponsor)
class Game2SponsorAdmin(admin.ModelAdmin):
    form = Game2SponsorForm
    list_display = [
        'id',
        'game_name',
        'sponsor_name',
        'created_at',
        'updated_at',
        'is_active',
    ]
