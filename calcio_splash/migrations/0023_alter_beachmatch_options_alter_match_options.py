# Generated by Django 4.0.4 on 2022-07-24 07:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calcio_splash', '0022_alter_match_next_match_alter_player_teams'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='beachmatch',
            options={'verbose_name_plural': 'Beach Matches'},
        ),
        migrations.AlterModelOptions(
            name='match',
            options={'verbose_name_plural': 'Matches'},
        ),
    ]
