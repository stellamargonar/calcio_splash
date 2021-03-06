# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-07-27 14:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calcio_splash', '0019_auto_20190718_2128'),
    ]

    operations = [
        migrations.CreateModel(
            name='BeachMatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_date_time', models.DateTimeField()),
                ('team_a_set_1', models.IntegerField(default=0)),
                ('team_b_set_1', models.IntegerField(default=0)),
                ('team_a_set_2', models.IntegerField(default=0)),
                ('team_b_set_2', models.IntegerField(default=0)),
                ('team_a_set_3', models.IntegerField(default=0)),
                ('team_b_set_3', models.IntegerField(default=0)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='beach_matches', to='calcio_splash.Group')),
                ('team_a', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='beach_matches_a', to='calcio_splash.Team')),
                ('team_b', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='beach_matches_b', to='calcio_splash.Team')),
            ],
        ),
    ]
