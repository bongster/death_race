# Generated by Django 2.1.2 on 2018-10-28 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commons', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='model_type',
            field=models.CharField(choices=[('g', 'GAME'), ('w', 'WOD')], default='w', max_length=10),
        ),
    ]