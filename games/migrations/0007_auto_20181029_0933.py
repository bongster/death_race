# Generated by Django 2.1.2 on 2018-10-29 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0006_auto_20181028_0815'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='team2game',
            unique_together={('team_id', 'game_id')},
        ),
    ]