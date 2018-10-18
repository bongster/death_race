from django.contrib import admin

# Register your models here.
from .models import Game, WOD, WOD2Game, Team, Team2Game, Record



@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['logo_image_tag', 'main_image_tag'] + [field.name for field in Game._meta.get_fields()]

@admin.register(WOD)
class WODAdmin(admin.ModelAdmin):
    list_display = [field.name for field in WOD._meta.get_fields()]

@admin.register(WOD2Game)
class WOD2GameAdmin(admin.ModelAdmin):
    list_display = [field.name for field in WOD2Game._meta.get_fields()]

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Team._meta.get_fields()]

@admin.register(Team2Game)
class Team2GameAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Team2Game._meta.get_fields()]

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Record._meta.get_fields()]
