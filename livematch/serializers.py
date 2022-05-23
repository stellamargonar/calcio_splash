from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from calcio_splash.models import Match, Team, Player, Goal


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


class MatchSerializer(serializers.ModelSerializer):
    team_a = TeamSerializer()
    team_b = TeamSerializer()

    class Meta:
        model = Match
        fields = ['pk', 'team_a', 'team_b', 'score_a', 'score_b']
