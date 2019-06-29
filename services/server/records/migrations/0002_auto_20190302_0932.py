# Generated by Django 2.1.5 on 2019-03-02 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_initial'),
        ('games', '0002_auto_20190302_0932'),
        ('records', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='m_team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='teams.Team'),
        ),
        migrations.AddField(
            model_name='record',
            name='m_wod',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='games.WOD'),
        ),
    ]