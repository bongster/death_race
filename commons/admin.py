from django.contrib import admin

# Register your models here.
from django.contrib.admin import register

from commons.forms import ResourceForm
from commons.models import Resource


@register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    form = ResourceForm
    list_display = [field.name for field in Resource._meta.get_fields()]

