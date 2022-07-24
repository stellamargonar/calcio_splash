from django.shortcuts import render
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from calcio_splash.models import Match, Team, Player, Goal, BeachMatch
from livematch.serializers import MatchSerializer, BeachMatchSerializer


def index(request):
    return render(request, "livematch/index.html")


# TODO rimuovere e mettere timezone now
YEAR = 2019


class MatchViewSet(ModelViewSet):
    serializer_class = MatchSerializer
    http_method_names = ['get', 'post']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Match.objects.filter(group__tournament__edition_year=YEAR).all().order_by('match_date_time')

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


class BeachMatchViewSet(ModelViewSet):
    serializer_class = BeachMatchSerializer
    http_method_names = ['get', 'post']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return BeachMatch.objects.filter(group__tournament__edition_year=YEAR).all().order_by('match_date_time')

    @action(detail=True, methods=['POST'])
    def score(self, request, pk):
        match = self.get_object()
        try:
            team = Team.objects.get(pk=request.data['teamId'])
        except Team.DoesNotExist:
            raise ValidationError()

        set_nr = request.data['set']
        remove = request.data.get('remove', False)
        to_add = 1 if not remove else -1
        is_a = team == match.team_a

        if set_nr == 1:
            match.team_a_set_1 += to_add if is_a else 0
            match.team_b_set_1 += to_add if not is_a else 0
        elif set_nr == 2:
            match.team_a_set_2 += to_add if is_a else 0
            match.team_b_set_2 += to_add if not is_a else 0
        else:
            match.team_a_set_3 += to_add if is_a else 0
            match.team_b_set_3 += to_add if not is_a else 0
        match.save()

        return self.retrieve(request, pk)

    @action(detail=True, methods=['POST'])
    def reset(self, request, pk):
        match = self.get_object()
        match.team_a_set_1 = 0
        match.team_b_set_1 = 0
        match.team_a_set_2 = None
        match.team_b_set_2 = None
        match.team_a_set_3 = None
        match.team_b_set_3 = None
        match.save()

        return self.retrieve(request, pk)

    @action(detail=True, methods=['POST'], url_path='add-set')
    def add_set(self, request, pk):
        match = self.get_object()
        if match.team_a_set_1 is None:
            match.team_a_set_1 = 0
            match.team_b_set_1 = 0
        elif match.team_a_set_2 is None:
            match.team_a_set_2 = 0
            match.team_b_set_2 = 0
        elif match.team_a_set_3 is None:
            match.team_a_set_3 = 0
            match.team_b_set_3 = 0
        match.save()

        return self.retrieve(request, pk)
