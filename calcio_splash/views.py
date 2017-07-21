from django.views.generic import DetailView, ListView
from calcio_splash.models import Group, Match, Player, Team, Tournament
from calcio_splash.helpers import AlboDoroHelper, GroupHelper, MatchHelper


class TeamListView(ListView):
    model = Team
    template_name = 'teams.html'
    context_object_name = 'team_list'

    def get_queryset(self):
        return Team.objects.all()


class TeamDetailView(DetailView):
    model = Team
    template_name = 'team.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['players'] = Player.objects.filter(team=context['object'].id)
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
        tournament.groups_clean = [
            GroupHelper.build_group(group)
            for group in tournament.groups.all()
        ]

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


def exception(request):
    1 / 0
