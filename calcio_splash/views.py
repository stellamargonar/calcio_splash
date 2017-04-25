from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView
from calcio_splash.models import Goal, Match, Player, Team, Tournament
from calcio_splash.helpers import GroupHelper, MatchHelper

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
        return Match.objects.all().order_by('-match_date_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['object_list'] = [
            MatchHelper.build_match(match) for match in context['object_list']
        ]
        return context

class MatchDetailView(DetailView):
    model = Match
    template_name = 'match.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['match'] = MatchHelper.build_match(context['match'])
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
