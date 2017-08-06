# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-03 17:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calcio_splash', '0013_group_is_final'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='player',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='goals', to='calcio_splash.Player'),
        ),
    ]