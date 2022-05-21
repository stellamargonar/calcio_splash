from rest_framework import serializers

from calcio_splash.models import Match, Team, Player


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['pk', 'name']


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
        fields = ['pk', 'team_a', 'team_b', 'score']
