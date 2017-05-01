from django import forms
from django.contrib import admin
from calcio_splash.models import Goal, Group, Match, Player, Team, Tournament


class TeamSelectField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.name

class GroupSelectField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.name


class MatchForm(forms.ModelForm):
    team_a = TeamSelectField(queryset=Team.objects.all())
    team_b = TeamSelectField(queryset=Team.objects.all())
    group = GroupSelectField(queryset=Group.objects.all())

    class Meta:
        model = Match
        exclude = ['next_match']


class TeamForm(forms.ModelForm):

    class Meta:
        model = Match
        exclude = ['next_match']

class PlayerAdminInline(admin.TabularInline):
    model = Player
