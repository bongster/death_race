from django.contrib import admin
from .models import Team2User

# Register your models here.


@admin.register(Team2User)
class Team2UserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Team2User._meta.get_fields()]
