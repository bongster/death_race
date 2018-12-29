import csv
import io

from django.urls import path
from django.shortcuts import redirect, render
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.contrib.auth.models import Group
from .models import User, MyUser
from commons.forms import CsvImportForm
from commons.utils import ExportCsvMixin
# Register your models here.

@admin.register(MyUser)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    # form = UserChangeForm
    # add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

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

admin.site.unregister(Group)