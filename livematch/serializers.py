from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from calcio_splash.models import Match, Team, Player, Goal, Group


class PlayerSerializer(serializers.ModelSerializer):
    score = SerializerMethodField()

    class Meta:
        model = Player
        fields = ['pk', 'name', 'score']

    def get_score(self, instance: Player) -> int:
        match = self.parent.parent.parent.instance
        if isinstance(match, QuerySet):
            match = match.first()
        return Goal.objects.filter(match=match, player=instance).count()


class TeamSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, source='player')

    class Meta:
        model = Team
        fields = ['pk', 'name', 'players']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['pk', 'name', 'tournament', 'is_final']


class MatchSerializer(serializers.ModelSerializer):
    team_a = TeamSerializer()
    team_b = TeamSerializer()
    date_time = SerializerMethodField()
    group = GroupSerializer()
    ended = SerializerMethodField()


    class Meta:
        model = Match
        fields = ['pk', 'team_a', 'team_b', 'score_a', 'score_b', 'date_time', 'group', 'ended']

    def get_date_time(self, instance: Match) -> str:
        return instance.match_date_time.strftime('%a %-d - %H:%M')

    def get_ended(self, instance: Match) -> bool:
        return instance.end_time is not None