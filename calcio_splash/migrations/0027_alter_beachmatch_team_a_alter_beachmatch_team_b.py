# Generated by Django 4.0.4 on 2022-07-29 10:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calcio_splash', '0026_beachmatch_ended'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beachmatch',
            name='team_a',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='beach_matches_a', to='calcio_splash.team'),
        ),
        migrations.AlterField(
            model_name='beachmatch',
            name='team_b',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='beach_matches_b', to='calcio_splash.team'),
        ),
    ]
