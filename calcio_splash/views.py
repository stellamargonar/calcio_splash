from datetime import datetime, timedelta

from django.db.models import Count, Q
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import DetailView, ListView, TemplateView

from calcio_splash.helpers import AlboDoroHelper, BracketsHelper, GroupHelper, MatchHelper
from calcio_splash.models import BeachMatch, Goal, Group, Match, Player, Team, Tournament


def can_show_gironi_and_matches(obj_year: int | str):
    if obj_year is None:
        return False
    tournament_year = int(obj_year)
    this_year = timezone.now().year
    if tournament_year < this_year:
        return True

    rilascio_gironi = datetime.strptime(f'{this_year}-07-28+07:00', '%Y-%m-%d%z')
    return timezone.now() >= rilascio_gironi


def handler404(request, exception=None):
    response = render(request, 'errors/404.html')
    response.status_code = 404
    return response


def handler500(request, exception=None):
    response = render(request, 'errors/500.html')
    response.status_code = 404
    return response


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not can_show_gironi_and_matches(timezone.now().year):
            return context

        context['match'] = self._get_current_match()
        context['next_match'] = self._get_next_match()

        context['match_beach'] = self._get_current_match(True)
        context['next_match_beach'] = self._get_next_match(True)

        return context

    def _get_current_match(self, is_beach=False):
        now = timezone.now()
        last_year = timezone.now() - timedelta(days=365)
        qs = None
        if is_beach:
            qs = BeachMatch.objects.filter(ended=False)
        else:
            qs = Match.objects.filter(end_time__isnull=True)
        return qs.filter(match_date_time__lte=now, match_date_time__gt=last_year).order_by('match_date_time').first()

    def _get_next_match(self, is_beach=False):
        now = timezone.now()
        qs = None
        if is_beach:
            qs = BeachMatch.objects.filter(ended=False)
        else:
            qs = Match.objects.filter(end_time__isnull=True)
        return qs.filter(match_date_time__gt=now).order_by('match_date_time').first()


class TeamDetailView(DetailView):
    model = Team
    template_name = 'team.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        team_id = context['object'].id
        # Add in a QuerySet of all the books
        context['players'] = Player.objects.filter(teams=team_id)
        context['matches'] = Match.objects.filter(Q(team_a=team_id) | Q(team_b=team_id)).order_by('match_date_time')
        context['matches'] = [MatchHelper.build_match(match)[0] for match in context['matches']]
        context['beach_matches'] = BeachMatch.objects.filter(Q(team_a=team_id) | Q(team_b=team_id)).order_by(
            'match_date_time'
        )

        return context


class MatchListView(ListView):
    model = Match
    template_name = 'matches.html'
    context_object_name = 'match_list'

    def get_queryset(self):
        year = self.kwargs['year']
        return Match.objects.filter(group__tournament__edition_year=year).order_by('match_date_time')

    def get_context_data(self, **kwargs):
        year = self.kwargs['year']
        context = super().get_context_data(**kwargs)

        if not can_show_gironi_and_matches(year):
            context.pop('match_list', None)
            return context

        context['year'] = year
        context['match_list'] = [MatchHelper.build_match(match)[0] for match in context['object_list']]
        context['beach_match_list'] = [
            match
            for match in BeachMatch.objects.filter(group__tournament__edition_year=year).order_by('match_date_time')
        ]
        return context


class MatchDetailView(DetailView):
    model = Match
    template_name = 'match.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        match = context['match']
        if not can_show_gironi_and_matches(match.group.tournament.edition_year):
            context.pop('match', None)
            return context
        context['match'], _ = MatchHelper.build_match(match)
        return context


class BeachMatchDetailView(DetailView):
    model = BeachMatch
    template_name = 'match.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        match = context['beachmatch']
        if not can_show_gironi_and_matches(match.group.tournament.edition_year):
            context.pop('match', None)
            return context
        context['match'] = match
        context['is_beach'] = True
        return context


class GroupDetailView(DetailView):
    model = Group
    template_name = 'group.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = context['group']
        if not can_show_gironi_and_matches(group.tournament.edition_year):
            context.pop('group', None)
            return context

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

        # non mostrare i gironi prima del 1 agosto
        if can_show_gironi_and_matches(tournament.edition_year):
            # load each group team stats
            tournament.groups_clean = [
                GroupHelper.build_group(group) for group in tournament.groups.filter(is_final=False)
            ]
            tournament.brackets = BracketsHelper.build_brackets(tournament)
        else:
            tournament.teams = Team.objects.filter(year=tournament.edition_year, gender=tournament.gender)

        AlboDoroHelper.build_albo(tournament)
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
        context['calcio'] = [
            AlboDoroHelper.build_albo(tournament)
            for tournament in context['object_list']
            if tournament.gender != Team.BEACH
        ]
        context['beach'] = [
            AlboDoroHelper.build_albo(tournament)
            for tournament in context['object_list']
            if tournament.gender == Team.BEACH
        ]
        context['year'] = self.kwargs['year']
        return context


class AlboMarcatori(ListView):
    model = Player
    template_name = 'albomarcatori.html'

    def get_queryset(self):
        gender = self.kwargs['gender']
        return Player.objects.filter(teams__gender=gender)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        player_id_set = set()
        player_classifica = []
        player_qs = context['object_list']

        agg_field = 'match__group__tournament__edition_year'
        for player in player_qs.only("id", "name", "surname", "nickname"):
            if player.pk in player_id_set:
                continue

            player_id_set.add(player.pk)

            agg = Goal.objects.filter(player__pk=player.pk).values(agg_field).annotate(dcount=Count(agg_field))

            player_data = {
                'player': player.full_name,
                'team': Team.objects.filter(player__pk=player.pk).last(),
            }

            player_data.update({item[agg_field]: item['dcount'] for item in agg})
            player_data['total'] = sum(item['dcount'] for item in agg)
            player_classifica.append(player_data)

        context['classifica'] = sorted(player_classifica, key=lambda x: (x['total'], x['player']), reverse=True)
        return context


def exception(request):
    1 / 0
