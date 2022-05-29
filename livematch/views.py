from django.shortcuts import render
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from calcio_splash.helpers import GroupHelper
from calcio_splash.models import Match, Team, Player, Goal, Tournament
from livematch.serializers import MatchSerializer


def index(request):
    return render(request, "livematch/index.html")


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

    @action(detail=False, methods=['POST'])
    def generate(self, request):
        # for tournament in Tournament.objects.filter(edition_year=YEAR):
        #     if 'beach' in tournament.name.lower():
        #         continue
        #     try:
        #         GroupHelper.generate_new_groups_for_calcio(tournament)
        #     except:
        #         pass

        beach = Tournament.objects.filter(edition_year=YEAR, name__icontains='beach').first()
        if beach:
            GroupHelper.generate_new_groups_for_beach(beach)

        return self.list(request)

