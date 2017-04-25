from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from calcio_splash.models import Goal, Match, Player, Team

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
            MatchDetailView.build_match(match) for match in context['object_list']
        ]
        return context

class MatchDetailView(DetailView):
    model = Match
    template_name = 'match.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['match'] = MatchDetailView.build_match(context['match'])
        return context
        
    @staticmethod
    def build_match(match):
        goals = Goal.objects.filter(match=match.id)

        # compute score
        team_a_score = 0
        team_b_score = 0
        for goal in goals:
            if goal.team == match.team_a:
                team_a_score += 1
            if goal.team == match.team_b:
                team_b_score += 1

        match.goals = goals
        match.team_a_score = team_a_score
        match.team_b_score = team_b_score

        return match
