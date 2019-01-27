from django.contrib import admin

from .models import Sponsor
from .forms import SponsorForm

# Register your models here.

@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    form = SponsorForm
    list_display = [
        'id',
        'name',
        'description',
        'image_link',
        'participated_game_list',
        'created_at',
        'updated_at',
        'is_active',
    ]
