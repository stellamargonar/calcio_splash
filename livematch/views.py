from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet

from calcio_splash.models import Match, Team, Player, Goal
from livematch.serializers import MatchSerializer


def index(request):
    return render(request, "livematch/index.html")


class MatchViewSet(ModelViewSet):
    serializer_class = MatchSerializer
    http_method_names = ['get' , 'post']

    def get_queryset(self):
        return Match.objects.all()

    @action(detail=True, methods=['POST'])
    def score(self, request, pk):
        match = self.get_object()
        try:
            team = Team.objects.get(pk=request.data['teamId'])
        except Team.DoesNotExist:
            raise ValidationError()
        player = None
        if request.data.get('playerId'):
            try:
                player = Player.objects.get(pk=request.data['playerId'], teams=team)
            except Player.DoesNotExist:
                raise ValidationError()
        Goal.objects.create(team=team, player=player, match=match, minute=0)
        return self.retrieve(request, pk)

    @action(detail=True, methods=['POST'])
    def reset(self, request, pk):
        Goal.objects.filter(match=self.get_object()).delete()
        return self.retrieve(request, pk)
