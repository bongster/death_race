from django.db import models

# Create your models here.

class User(models.Model):
    MALE = 'male'
    FEMALE = 'female'

    GENTER_TYPE = (
        (MALE, 'MALE'),
        (FEMALE, 'FEMALE'),
    )

    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    profile_url = models.URLField(blank=True, null=True)
    gender = models.CharField(
        choices=GENTER_TYPE, 
        default=MALE,
         max_length=10
    )


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '({}) {}'.format(self.id, self.name)

    def __str__(self):
        return '({}) {}'.format(self.id, self.name)