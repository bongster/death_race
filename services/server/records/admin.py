import csv
import io

from commons.utils import ExportCsvMixin
from commons.forms import CsvImportForm
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect, render
from death_race.utils import get_or_none

from .models import Record
from .forms import RecordForm
from commons.models import Resource
from teams.models import Team
from games.models import WOD

# Register your models here.

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
