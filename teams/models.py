from django.db import models
from games.models import Team
from django.contrib.auth import get_user_model

# Create your models here.


class Team2User(models.Model):
    class Meta:
        db_table = 'teams_2_users'

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)