# Generated by Django 2.1.2 on 2018-10-26 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_auto_20181026_1522'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team2Competition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_id', models.IntegerField()),
                ('competition_id', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'teams_2_competitions',
            },
        ),
        migrations.DeleteModel(
            name='Game2Competition',
        ),
    ]
