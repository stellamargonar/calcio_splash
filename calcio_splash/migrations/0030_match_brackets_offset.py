# Generated by Django 4.2.14 on 2024-08-04 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calcio_splash', '0029_player_nickname'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='brackets_offset',
            field=models.IntegerField(default=0),
        ),
    ]
