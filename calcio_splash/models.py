from django.db import models
from django.contrib import admin

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return u'{}'.format(self.name)

class Player(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)


class Tournament(models.Model):
    name = models.CharField(max_length=250)
    edition_year = models.IntegerField()


class Group(models.Model):
    name = models.CharField(max_length=50)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='groups')


class Match(models.Model):
    team_a = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_a')
    team_b = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_b')
    match_date_time = models.DateTimeField()

    next_match = models.ForeignKey('self', null=True, related_name='prev_matches')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='matches')


class Goal(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='goals')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='goals')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='goals')
    minute = models.IntegerField()
