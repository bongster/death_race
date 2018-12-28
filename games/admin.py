import csv
import io

from django.contrib import admin

# Register your models here.
from django.shortcuts import redirect, render
from django.urls import path

from commons.forms import CsvImportForm
from commons.utils import ExportCsvMixin
from death_race.utils import get_or_none
from .models import Game, WOD, WOD2Game, Team, Team2Game, Record, Competition, Game2Sponsor
from commons.models import Resource
from .forms import WOD2GameForm, Team2GameForm, RecordForm, WODForm, CompetitionForm, Game2SponsorForm
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


# @admin.register(WOD2Game)
# class WOD2GameAdmin(admin.ModelAdmin):
#     form = WOD2GameForm
#     list_display = [field.name for field in WOD2Game._meta.get_fields()]


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'team_type',
        'gender_type',
        'created_at',
        'updated_at',
        'is_active',
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


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin, ExportCsvMixin):
    form = RecordForm
    list_display = [
        'id',
        'wod_name',
        'team_name',
        'score',
        'point',
        'is_active',
        'video_url',
    ]
    actions = ['export_as_csv']

    change_list_template = 'entities/import_csv.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == 'POST':
            team_name_ids = {}
            wod_name_ids = {}
            csv_file = io.TextIOWrapper(request.FILES['csv_file'].file, encoding=request.encoding)
            reader = csv.DictReader(csv_file)
            count = 0
            for row in reader:
                team_name = row['team_name']
                wod_name = row['wod_name']

                team_id = team_name_ids.get(team_name)
                if not team_id:
                    print('team_name: {}'.format(team_name))
                    team_name_ids[team_name] = Team.objects.get(name=team_name).id
                    team_id = team_name_ids[team_name]

                wod_id = wod_name_ids.get(wod_name)

                if not wod_id:
                    wod_name_ids[wod_name] = WOD.objects.get(name=wod_name).id
                    wod_id = wod_name_ids[wod_name]

                if team_id and wod_id:
                    print('team_id: {}, wod_id: {}'.format(team_id, wod_id))
                    record = get_or_none(
                        Record,
                        wod_id=wod_id,
                        team_id=team_id,
                    )
                    if not record:
                        record = Record(
                            wod_id=wod_id,
                            team_id=team_id,
                        )

                    record.is_active = row['is_active']
                    record.point = row['point']
                    record.score = row['score']
                    record.save()

                    # TODO: set record resource video url
                    video_url = row.get('video_url')
                    if video_url:
                        resource = get_or_none(Resource,
                            model_type=Resource.MODEL_TYPE_RECORD,
                            model_id=record.id,
                        )

                        if resource:
                            resource.link = video_url
                            resource.is_active=True
                        else:
                            resource = Resource(
                                model_type=Resource.MODEL_TYPE_RECORD,
                                model_id=record.id,
                                link = video_url,
                                is_active=True,
                            )
                        resource.save()
                    count += 1
            # Create Hero objects from passed in data
            # ...
            self.message_user(request, 'Your csv file has been imported: created or updated {}'.format(count))
            return redirect('..')
        form = CsvImportForm()
        payload = {'form': form}
        return render(
            request, 'admin/csv_form.html', payload
        )

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
