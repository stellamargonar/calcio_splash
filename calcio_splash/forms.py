from django import forms
from django.contrib import admin
from django.utils import timezone

from calcio_splash.models import Group, Match, Player, Team


class TeamSelectField(forms.ModelChoiceField):
    def _get_symbol_for_team(self, team):
        if team.gender == Team.BEACH:
            return '🏖'
        if team.gender == Team.FEMALE:
            return '♀'
        return '♂'

    def label_from_instance(self, obj):
        return f'{self._get_symbol_for_team(obj)} {obj.name} ({obj.year})'


class GroupSelectField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class MatchForm(forms.ModelForm):
    team_a = TeamSelectField(queryset=Team.objects.filter(year=timezone.now().year).all())
    team_b = TeamSelectField(queryset=Team.objects.filter(year=timezone.now().year).all())
    group = GroupSelectField(queryset=Group.objects.filter(tournament__edition_year=timezone.now().year).all())

    class Meta:
        model = Match
        exclude = ['next_match']


class TeamForm(forms.ModelForm):
    class Meta:
        model = Match
        exclude = ['next_match']


class PlayerAdminInline(admin.TabularInline):
    model = Player.teams.through
