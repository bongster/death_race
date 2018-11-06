import csv
import io

from django.urls import path
from django.shortcuts import redirect, render
from django.contrib import admin

from .models import Team2User
from games.models import Team
from users.models import User
from commons.forms import CsvImportForm
from commons.utils import ExportCsvMixin

# Register your models here.


@admin.register(Team2User)
class Team2UserAdmin(ExportCsvMixin, admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'team',
        'created_at',
        'updated_at',
        'is_active'
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
            csv_file = io.TextIOWrapper(request.FILES['csv_file'].file, encoding=request.encoding)
            reader = csv.DictReader(csv_file)
            count = 0
            for row in reader:
                team_name = row['team_name']
                email = row['email']
                user_email_id_map = {}
                team_name_id_map = {}
                is_active = row['is_active']

                user_id = user_email_id_map.get(email)
                if not user_id:
                    user_email_id_map[email] = User.objects.get(
                        email=email,
                    ).id
                    user_id = user_email_id_map[email]
                
                team_id = team_name_id_map.get(team_name)
                if not team_id:
                    team_name_id_map[team_name] = Team.objects.get(
                        name=team_name,
                        is_active=True,
                    ).id
                    team_id = team_name_id_map[team_name]
                
                if Team2User.objects.filter(
                    team_id=team_id,
                    user_id=user_id,
                ).exists():
                    t2u = Team2User.objects.get(
                        team_id=team_id,
                        user_id=user_id,
                    )
                    t2u.is_active = is_active
                else:
                    t2u = Team2User(
                        team_id=team_id,
                        user_id=user_id,
                        is_active=is_active,
                    )
                t2u.save()
                count += 1
            self.message_user(request, 'Your csv file has been imported: created or updated {}'.format(count))
            return redirect('..')
        form = CsvImportForm()
        payload = {'form': form}
        return render(
            request, 'admin/csv_form.html', payload
        )
