from django.db import models
from users.models import User

# Create your models here.

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

    def __unicode__(self):
        return '({}) {}'.format(self.id, self.name)

    def __str__(self):
        return '({}) {}'.format(self.id, self.name)


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