import csv
import io

from django.urls import path
from django.shortcuts import redirect, render
from django.contrib import admin

from .models import User
from commons.forms import CsvImportForm
from commons.utils import ExportCsvMixin
# Register your models here.


@admin.register(User)
class UserAdmin(ExportCsvMixin, admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'email',
        'profile_url',
        'created_at',
        'updated_at',
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
                name = row['name']
                email = row['email']
                gender = row['gender']
                profile_url = row.get('profile_url')
                if User.objects.filter(
                    email=email,
                ).exists():
                    u = User.objects.get(
                        email=email,
                    )
                else:
                    u = User(
                        email=email,
                        gender=gender,
                    )
                u.name = name
                u.gender = gender
                if profile_url:
                    u.profile_url = profile_url
                u.save()
                count += 1
            self.message_user(request, 'Your csv file has been imported: created or updated {}'.format(count))
            return redirect('..')
        form = CsvImportForm()
        payload = {'form': form}
        return render(
            request, 'admin/csv_form.html', payload
        )
