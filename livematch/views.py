from django.shortcuts import render
from django.utils import timezone
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
        return Match.objects.filter(group__tournament__edition_year=2019).all().order_by('match_date_time')

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

        remove = request.data.get('remove', False)
        if remove:
            latest_goal = Goal.objects.filter(team=team, player=player, match=match).last()
            if latest_goal is not None:
                latest_goal.delete()
        else:
            Goal.objects.create(team=team, player=player, match=match, minute=0)
        return self.retrieve(request, pk)

    @action(detail=True, methods=['POST'])
    def reset(self, request, pk):
        Goal.objects.filter(match=self.get_object()).delete()
        return self.retrieve(request, pk)

    @action(detail=True, methods=['POST'])
    def lock(self, request, pk):
        match = self.get_object()
        match.end_time = timezone.now()
        match.save()
        return self.retrieve(request, pk)

    @action(detail=True, methods=['POST'])
    def unlock(self, request, pk):
        match = self.get_object()
        match.end_time = None
        match.save()
        return self.retrieve(request, pk)
