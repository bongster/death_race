from django.db import models

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

    logo_image = models.ImageField(blank=True)
    main_image = models.ImageField(blank=True)
    description = models.TextField(blank=True)

    start_date = models.DateTimeField(blank=True)
    end_date = models.DateTimeField(blank=True)

    is_active = models.BooleanField(default=False)

class WOD2game(models.Model):
    """
    included wods in game
    """
    class Meta:
        db_table = "wods_2_games"
        unique_together = [
            ("game_id", "wod_id"),
        ]
    
    game_id = models.IntegerField()
    wod_id = models.IntegerField()
    order = models.PositiveSmallIntegerField()

    is_ative = models.BooleanField(default=False)

class WOD(models.Model):
    """
    workout of daily

    name
    is_active

    """
    class Meta:
        db_table = "wods"

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
    description = models.TextField(blank=True)
    video_link = models.URLField(max_length=200)

    is_active = models.BooleanField(default=False)

class Team(models.Model):
    class Meata:
        db_table = "teams"

    INDIVIDUAL = "individual"
    TEAM = "team"

    TEAM_TYPE = (
        (INDIVIDUAL, "individual"),
        (TEAM, "team"),
    )

    MALE = "male"
    FEMALE = "female"
    MIXED = "mixed"

    GENTER_TYPE = (
        (MALE, "MALE"),
        (FEMALE, "FEMALE"),
        (MIXED, "MIXED",)
    )

    name = models.CharField(max_length=50)
    team_type = models.CharField(choices=TEAM_TYPE, default=TEAM, max_length=50)
    gender_type = models.CharField(choices=GENTER_TYPE, default=MALE, max_length=10)

    is_active = models.BooleanField(default=True)

class Team2Game(models.Model):
    """
    included team in games

    do not use same team different game

    """
    class Meta:
        db_table = 'teams_2_games'
        unique_together = (
            ('team_id', 'game_id'),
        )
    
    team_id = models.PositiveSmallIntegerField()
    game_id = models.PositiveSmallIntegerField()

    is_active = models.BooleanField(default=False)

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
    team_id = models.IntegerField()

    score = models.CharField(max_length=100)
    point = models.PositiveSmallIntegerField()

    is_ative = models.BooleanField(default=False)
