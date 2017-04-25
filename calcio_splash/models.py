from django.db import models
from django.contrib import admin

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=100)
    # question_text = models.CharField(max_length=200)
    # pub_date = models.DateTimeField('date published')

class Player(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

class Match(models.Model):
    team_a = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_a')
    team_b = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_b')
    match_date_time = models.DateTimeField()

    # aggiungere risultati

class Goal(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='match')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player')
    minute = models.IntegerField()

admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Match)
admin.site.register(Goal)
