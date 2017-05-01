from django.contrib import admin
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponseServerError

from calcio_splash.models import Goal, Group, Match, Player, Team, Tournament
from calcio_splash.helpers import MatchHelper

class CalcioSplashAdminSite(admin.AdminSite):
    def get_urls(self):
        from django.conf.urls import url
        urls = super().get_urls()
        # Note that custom urls get pushed to the list (not appended)
        # This doesn't work with urls += ...
        urls = urls + [
            url(r'match_goals/(?P<id>\d+)$', MatchGoalAdmin.as_view(), name='match-goals'),
            url(r'^score_goal/$', create_goal),

        ]
        return urls

admin_site = CalcioSplashAdminSite()


class TeamAdmin(admin.ModelAdmin):
    list_display = ['name']

admin_site.register(Team, TeamAdmin)


class PlayerAdmin(admin.ModelAdmin):
    list_display = ['surname', 'name']

admin_site.register(Player, PlayerAdmin)


class MatchAdmin(admin.ModelAdmin):
    list_display = ['team_a', 'team_b']

admin_site.register(Match, MatchAdmin)


class GroupAdmin(admin.ModelAdmin):
    list_display = ['name']

admin_site.register(Group, GroupAdmin)


class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'edition_year']

admin_site.register(Tournament, TournamentAdmin)


class MatchGoalAdmin(TemplateView, admin.ModelAdmin):
    template_name = 'admin/match_goal.html'

    def get_context_data(self, id, **kwargs):
        context = super().get_context_data(**kwargs)
        match = Match.objects.get(id=id)

        context['match'] = MatchHelper.build_match(match)
        return context

def create_goal(request):
    error_msg = u"No POST data sent."
    if request.method == "POST":
        post = request.POST.copy()
        print(post)
        if post.has_key('team') and post.has_key('player'):
            team = post['team']
            player = post['player']
            match = post['match']

            new_goal = Goal.objects.create(team=team, player=player, match=match)
            return HttpResponseRedirect()
        else:
            error_msg = u"Insufficient POST data (need 'player, match and team')"
    return HttpResponseServerError(error_msg)
