# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-15 16:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calcio_splash', '0014_auto_20170803_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='year',
            field=models.IntegerField(default=2017),
        ),
    ]
