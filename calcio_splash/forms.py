from django import forms
from django.contrib import admin
from django.utils import timezone

from calcio_splash.models import Group, Match, Player, BeachMatch


class GroupSelectField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class MatchForm(forms.ModelForm):
    group = GroupSelectField(queryset=Group.objects.filter(tournament__edition_year=timezone.now().year).all())

    class Meta:
        model = Match
        exclude = []


class BeachMatchForm(MatchForm):
    class Meta:
        model = BeachMatch
        exclude = []


class TeamForm(forms.ModelForm):
    class Meta:
        model = Match
        exclude = []


class PlayerAdminInline(admin.TabularInline):
    model = Player.teams.through
    raw_id_fields = ('player', )