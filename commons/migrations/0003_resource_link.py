# Generated by Django 2.1.2 on 2018-10-28 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commons', '0002_auto_20181028_1128'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='link',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
    ]