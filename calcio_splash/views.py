from django.db.models import Count
from django.utils import timezone
from django.views.generic import DetailView, ListView

from calcio_splash.models import Group, Match, Player, Team, Tournament, Goal
from calcio_splash.helpers import AlboDoroHelper, GroupHelper, MatchHelper


class TeamListView(ListView):
    model = Team
    template_name = 'teams.html'
    context_object_name = 'team_list'

    def get_queryset(self):
        return Team.objects.filter(year=timezone.now().year).all()


class TeamDetailView(DetailView):
    model = Team
    template_name = 'team.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['players'] = Player.objects.filter(team=context['object'].id)
        context['matches'] = Match.objects.filter(team_a=context['object'].id)
        context['matches'] = context['matches'] | Match.objects.filter(team_b=context['object'].id)
        context['matches'].order_by('match_date_time')
        context['matches'] = [
            MatchHelper.build_match(match)[0] for match in context['matches']
        ]
        return context


class MatchListView(ListView):
    model = Match
    template_name = 'matches.html'
    context_object_name = 'match_list'

    def get_queryset(self):
        group_id = self.kwargs['pk_group']
        return Match.objects.filter(group__id=group_id).order_by('-match_date_time')

    def get_context_data(self, **kwargs):
        print(kwargs)

        context = super().get_context_data(**kwargs)

        context['object_list'] = [
            MatchHelper.build_match(match)[0] for match in context['object_list']
        ]
        return context


class MatchDetailView(DetailView):
    model = Match
    template_name = 'match.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['match'], _ = MatchHelper.build_match(context['match'])
        return context


class GroupDetailView(DetailView):
    model = Group
    template_name = 'group.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = context['group']

        # load each group team stats
        group = GroupHelper.build_group(group)

        context['group'] = group

        return context


class TournamentDetailView(DetailView):
    model = Tournament
    template_name = 'tournament.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tournament = context['tournament']

        # load each group team stats
        tournament.groups_clean = sorted([
            GroupHelper.build_group(group)
            for group in tournament.groups.all()
        ], key=lambda x: (-len(x.group_matches), x.id))

        context['tournament'] = tournament

        return context


class AlboView(ListView):
    model = Tournament
    template_name = 'albodoro.html'

    def get_queryset(self):
        year = self.kwargs['year']
        return Tournament.objects.filter(edition_year=year)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = [
            AlboDoroHelper.build_albo(tournament) for tournament in context['object_list']
        ]
        return context


class AlboMarcatori(ListView):
    model = Player
    template_name = 'albomarcatori.html'

    def get_queryset(self):
        gender = self.kwargs['gender']
        return Player.objects.filter(team__gender=gender)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        player_classifica = []
        player_qs = context['object_list']

        players_sorted = player_qs.values('name', 'surname')\
            .annotate(score=Count('goals'))\
            .order_by('-score')

        agg_field = 'match__group__tournament__edition_year'
        for player in players_sorted:
            agg = Goal.objects\
                .filter(player__name=player['name'], player__surname=player['surname'])\
                .values(agg_field)\
                .annotate(dcount=Count(agg_field))

            player_data = {
                'player': '{} {}'.format(player['name'], player['surname']),
                'total': player['score'],
                'team': Team.objects.filter(player__surname=player['surname'], player__name=player['name']).last(),
            }
            player_data.update({
                item[agg_field]: item['dcount']
                for item in agg
            })
            player_classifica.append(player_data)

        context['classifica'] = player_classifica
        return context


def exception(request):
    1 / 0
