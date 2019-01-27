from django.db import models

class Sponsor(models.Model):
    class Meta:
        db_table = 'sponsors'

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, default='')
    image_link = models.URLField(null=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def participated_game_list(self):
        from games.models import Game, Game2Sponsor
        return ','.join(
            [
                game.name for game in Game.objects.filter(
                    pk__in=Game2Sponsor.objects.filter(
                        sponsor_id=self.id,
                        is_active=True
                    ).values_list('game_id', flat=True)
                )
            ]
        )
