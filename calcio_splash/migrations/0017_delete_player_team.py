# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-15 17:14
from __future__ import unicode_literals

from django.db import migrations, models



class Migration(migrations.Migration):
    dependencies = [
        ('calcio_splash', '0016_player_teams'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='team',
        ),
    ]
