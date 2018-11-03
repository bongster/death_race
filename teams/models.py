from django.db import models
from games.models import Team
from users.models import User

# Create your models here.


class Team2User(models.Model):
    class Meta:
        db_table = 'teams_2_users'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)