# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-07 13:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calcio_splash', '0007_auto_20170507_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='gender',
            field=models.CharField(choices=[('M', 'Maschile'), ('F', 'Femminile')], default='M', max_length=2),
        ),
    ]
