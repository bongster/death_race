from django.db import models

from commons.models import Resource
from death_race.utils import get_or_none
from django.utils.html import format_html
from games.models import WOD
from teams.models import Team


# Create your models here.
class Record(models.Model):
    """
    team wod record data
    """
    class Meta:
        db_table = "records"
        unique_together = (
            ('wod_id', 'team_id'),
        )
    
    wod_id = models.IntegerField()
    team_id = models.IntegerField(db_index=True)

    m_wod = models.ForeignKey(
        'games.WOD',
        on_delete=models.CASCADE,
        blank = True,
        null=True,
    )

    m_team = models.ForeignKey(
        'teams.Team',
        on_delete=models.CASCADE,
        blank = True,
        null=True,
    )

    score = models.CharField(max_length=100)
    point = models.PositiveSmallIntegerField(null=True)

    is_active = models.BooleanField(default=False)

    def wod_name(self):
        return WOD.objects.get(pk=self.wod_id).name

    def team_name(self):
        team = Team.objects.get(pk=self.team_id)
        return format_html(
            '{} [ <b>{}</b> ]',
            team.name,
            team.team_type,
        )
    
    def video_url(self):
        resource = get_or_none(Resource,
            model_type=Resource.MODEL_TYPE_RECORD,
            model_id=self.id,
            is_active=True,
        )
        if resource:
            return resource.link