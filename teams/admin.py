from django.contrib import admin
from .models import Team2User

# Register your models here.


@admin.register(Team2User)
class Team2UserAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'team',
        'created_at',
        'updated_at',
        'is_active'
    ]
