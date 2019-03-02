from django.db import models
from django.conf import settings
from django.utils.html import format_html

from death_race.utils import get_or_none
from commons.models import Resource
from teams.models import Team
from sponsors.models import Sponsor


class Game(models.Model):
    """
    TABLE:
        games

    PARAMS:
        name
        logo_image
        main_image
        description

        start_date
        end_date
        is_active
    """
    class Meta:
        db_table = "games"

    name = models.CharField(max_length=100)
    logo_image = models.ImageField(blank=True, upload_to='games/')
    description = models.TextField(blank=True, default='')

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=False)

    def logo_image_tag(self):
        image_url = '{}{}'.format(settings.MEDIA_URL, self.logo_image)
        return format_html(
            "<a href='{}' target='_blank' ><img src='{}{}' width='144px'></a>",
            image_url,
            settings.MEDIA_URL,
            self.logo_image,
        )

    def competition_list(self):

        return format_html(
            '{}',
            Competition.objects.filter(
                game_id=self.id,
                is_active=True,
            ).values('name')
        )

    def sponed_sponsor_list(self):
        return format_html(
            '{}',
            Sponsor.objects.filter(
                pk__in=Game2Sponsor.objects.filter(
                    game_id=self.id,
                    is_active=True
                ).values_list('sponsor_id', flat=True)
            ).values('name')
        )

    def resources(self):
        return Resource.objects.filter(
            model_type=Resource.MODEL_TYPE_GAME,
            model_id=self.id,
            is_active=True,
        ).order_by('order')


class Competition(models.Model):
    """
    Competition model
    relationship
    game : competition == 1: N

    TODO: game: competition == N:N if required
    """
    name = models.CharField(max_length=255, default='')
    game_id = models.IntegerField(null=True)
    m_game = models.ForeignKey(
        'Game',
        on_delete=models.CASCADE,
        blank = True,
        null=True,
)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def game_name(self):
        game = Game.objects.filter(id=self.game_id)
        if game:
            return game[0].name

    def wod_list(self):
        return format_html('{}', ','.join(
            [
                wod['name']for wod in WOD.objects.filter(competition_id=self.id).values('name')
            ]
        ))


class Team2Competition(models.Model):
    """
    Deprecated
    """
    class Meta:
        db_table = 'teams_2_competitions'

    team_id = models.IntegerField()
    competition_id = models.IntegerField()

    m_team = models.ForeignKey(
        'teams.Team',
        on_delete=models.CASCADE,
        blank = True,
        null=True,
    )
    m_competition = models.ForeignKey(
        'Competition',
        on_delete=models.CASCADE,
        blank = True,
        null=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class WOD2Game(models.Model):
    """
    included wods in game
    Deprecated
    """
    class Meta:
        db_table = 'wods_2_games'
        unique_together = [
            ('game_id', 'wod_id', 'order'),
        ]
    
    game_id = models.IntegerField()
    wod_id = models.IntegerField()

    m_game = models.ForeignKey(
        'Game',
        on_delete=models.CASCADE,
        blank = True,
        null=True,
    )
    m_wod = models.ForeignKey(
        'WOD',
        on_delete=models.CASCADE,
        blank = True,
        null=True,
    )
    
    order = models.PositiveSmallIntegerField()

    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class WOD(models.Model):
    """
    workout of daily

    name
    is_active

    competition_id: included competition id

    """
    class Meta:
        db_table = 'wods'

    AMRAP = 'amrap'
    EMOM = 'emom'
    FOR_TIME = 'for_time'

    WOD_TYPE = (
        (AMRAP, 'amrap'),
        (EMOM, 'emom'),
        (FOR_TIME, 'for_time'),
    )

    name = models.CharField(max_length=100)
    wod_type = models.CharField(choices=WOD_TYPE, default=FOR_TIME, max_length=15)
    description = models.TextField(blank=True, default='')

    competition_id = models.IntegerField(null=True)

    m_competition = models.ForeignKey(
        'Competition',
        models.SET_NULL,
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def competition_name(self):
        competition = get_or_none(Competition, id=self.competition_id)
        if competition:
            return competition.name

        return ''

    def resources(self):
        return Resource.objects.filter(
            model_type=Resource.MODEL_TYPE_WOD,
            model_id=self.id,
            is_active=True,
        ).order_by('order')


class WOD2Competition(models.Model):
    """
    included wods in game
    not used
    Deprecated
    """

    class Meta:
        db_table = 'wods_2_competitions'
        unique_together = [
            ('competition_id', 'wod_id', 'order'),
        ]

    competition_id = models.IntegerField()
    wod_id = models.IntegerField()

    m_competition = models.ForeignKey(
        'Competition',
        on_delete=models.CASCADE,
        blank = True,
        null=True,
    )

    m_wod = models.ForeignKey(
        'WOD',
        on_delete=models.CASCADE,
        blank = True,
        null=True,
    )
    
    order = models.PositiveSmallIntegerField()

    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Team2Game(models.Model):
    """
    included team in games

    do not use same team different game

    """
    class Meta:
        db_table = 'teams_2_games'
        unique_together = (
            ('team_id', 'game_id')
        )
    
    team_id = models.PositiveSmallIntegerField(db_index=True)
    game_id = models.PositiveSmallIntegerField(db_index=True)

    m_team = models.ForeignKey(
        'teams.Team',
        on_delete=models.CASCADE,
        blank = True,
        null=True,
    )

    m_game = models.ForeignKey(
        'Game',
        on_delete=models.CASCADE,
        blank = True,
        null=True,
    )

    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def team_name(self):
        return Team.objects.get(id=self.team_id).name

    def game_name(self):
        return Game.objects.get(id=self.game_id).name

class Game2Sponsor(models.Model):
    class Meta:
        db_table = 'games_2_sponsors'
        unique_together = (
            ('game_id', 'sponsor_id'),
        )

    game_id = models.IntegerField(db_index=True)
    sponsor_id = models.IntegerField(db_index=True)

    m_game = models.ForeignKey(
        'Game',
        on_delete=models.CASCADE,
        blank = True,
        null=True,
    )

    m_sponsor = models.ForeignKey(
        'sponsors.Sponsor',
        on_delete=models.CASCADE,
        blank = True,
        null=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def game_name(self):
        return Game.objects.get(pk=self.game_id).name

    def sponsor_name(self):
        return Sponsor.objects.get(pk=self.sponsor_id).name
