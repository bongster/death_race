from django.db import models
from django.conf import settings
from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver
from django.utils.html import format_html

from death_race.utils import get_or_none
from commons.models import Resource


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
    main_image = models.ImageField(blank=True, upload_to='games/')
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

    def main_image_tag(self):
        image_url = '{}{}'.format(settings.MEDIA_URL, self.main_image)
        return format_html(
            "<a href='{}' target='_blank' ><img src='{}{}' width='144px'></a>",
            image_url,
            settings.MEDIA_URL,
            self.main_image,
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
    class Meta:
        db_table = 'teams_2_competitions'

    team_id = models.IntegerField()
    competition_id = models.IntegerField()
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class WOD2Game(models.Model):
    """
    included wods in game
    """
    class Meta:
        db_table = 'wods_2_games'
        unique_together = [
            ('game_id', 'wod_id', 'order'),
        ]
    
    game_id = models.IntegerField()
    wod_id = models.IntegerField()
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
    video_link = models.URLField(max_length=200, default='', blank=True)
    image_link = models.URLField(max_length=200, default='', blank=True)

    competition_id = models.IntegerField(null=True)

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
    """

    class Meta:
        db_table = 'wods_2_competitions'
        unique_together = [
            ('competition_id', 'wod_id', 'order'),
        ]

    competition_id = models.IntegerField()
    wod_id = models.IntegerField()
    order = models.PositiveSmallIntegerField()

    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Team(models.Model):
    class Meta:
        db_table = 'teams'

    INDIVIDUAL = 'individual'
    TEAM = 'team'

    TEAM_TYPE = (
        (INDIVIDUAL, 'individual'),
        (TEAM, 'team'),
    )

    MALE = 'male'
    FEMALE = 'female'
    MIXED = 'mixed'

    GENTER_TYPE = (
        (MALE, 'MALE'),
        (FEMALE, 'FEMALE'),
        (MIXED, 'MIXED',)
    )

    name = models.CharField(max_length=50)
    team_type = models.CharField(choices=TEAM_TYPE, default=TEAM, max_length=50)
    gender_type = models.CharField(choices=GENTER_TYPE, default=MALE, max_length=10)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


@receiver(pre_delete, sender=Team)
def pre_delete_team(sender, instance, using, **kwargs):
    Team2Game.objects.filter(
        team_id=instance.id
    ).delete()

    Record.objects.filter(
        team_id=instance.id
    ).delete()


@receiver(post_delete, sender=Team)
def post_delete_team(sender, instance, using, **kwargs):
    # team 삭제시에 team2competition에 있는 데이터도 제거.
    pass


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

    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def team_name(self):
        return Team.objects.get(id=self.team_id).name

    def game_name(self):
        return Game.objects.get(id=self.game_id).name

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


class Game2Sponsor(models.Model):
    class Meta:
        db_table = 'games_2_sponsors'
        unique_together = (
            ('game_id', 'sponsor_id'),
        )

    game_id = models.IntegerField(db_index=True)
    sponsor_id = models.IntegerField(db_index=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def game_name(self):
        return Game.objects.get(pk=self.game_id).name

    def sponsor_name(self):
        return Sponsor.objects.get(pk=self.sponsor_id).name
