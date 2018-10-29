import csv
import io

from django.contrib import admin

# Register your models here.
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import path

from commons.forms import CsvImportForm
from death_race.utils import get_or_none
from .models import Game, WOD, WOD2Game, Team, Team2Game, Record, Competition, Sponsor, Game2Sponsor
from .forms import WOD2GameForm, Team2GameForm, RecordForm, WODForm, CompetitionForm, SponsorForm, Game2SponsorForm


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
    list_display = [field.name for field in WOD._meta.get_fields()] + [
        'competition_name',
    ]


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


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin, ExportCsvMixin):
    form = RecordForm
    list_display = [
        'id',
        'wod_name',
        'team_name',
        'score',
        'point',
        'is_active'
    ]
    actions = ["export_as_csv"]

    change_list_template = "entities/records_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
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
                    count += 1
            # Create Hero objects from passed in data
            # ...
            self.message_user(request, "Your csv file has been imported: created or updated {}".format(count))
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "admin/csv_form.html", payload
        )

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


@admin.register(Game2Sponsor)
class Game2SponsorAdmin(admin.ModelAdmin):
    form = Game2SponsorForm
    list_display = [field.name for field in Game2Sponsor._meta.get_fields()]
