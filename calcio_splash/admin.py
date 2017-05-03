from django import forms
from django.contrib import admin
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseServerError

from calcio_splash.models import Goal, Group, Match, Player, Team, Tournament
from calcio_splash.helpers import MatchHelper
from calcio_splash.forms import MatchForm, PlayerAdminInline

class CalcioSplashAdminSite(admin.AdminSite):
    def get_urls(self):
        from django.conf.urls import url
        urls = super().get_urls()
        # Note that custom urls get pushed to the list (not appended)
        # This doesn't work with urls += ...
        urls = urls + [
            url(r'match_goals/(?P<id>\d+)$', MatchGoalAdmin.as_view(), name='match-goals'),
            url(r'match_goals/(?P<id>\d+)/score_goal$', create_goal),

        ]
        return urls

admin_site = CalcioSplashAdminSite()


class TeamAdmin(admin.ModelAdmin):
    inlines = (PlayerAdminInline, )
    list_display = ['name']

admin_site.register(Team, TeamAdmin)


class PlayerAdmin(admin.ModelAdmin):
    list_display = ['surname', 'name']

admin_site.register(Player, PlayerAdmin)


class MatchAdmin(admin.ModelAdmin):
    list_display = ['get_group', 'get_team_a', 'get_team_b']
    form = MatchForm
    actions = ['go_to_match_page']

    def get_group(self, obj):
        return obj.group.name

    def get_team_a(self, obj):
        return obj.team_a.name

    def get_team_b(self, obj):
        return obj.team_b.name

    def go_to_match_page(modeladmin, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect("admin/match_goals/" + selected[0] )

    get_group.short_description = 'Group'
    get_team_a.short_description = 'Team A'
    get_team_b.short_description = 'Team B'
    go_to_match_page.short_description = 'Start Match'

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

def create_goal(request, id):
    error_msg = u"No POST data sent."
    if request.method == "POST":
        post = request.POST.copy()
        if post.get('team') and post.get('player'):
            team = post['team']
            player = post['player']
            minute = post['minute']
            matchId = id
            new_goal = Goal.objects.create(
                team=Team.objects.get(pk=team),
                player=Player.objects.get(pk=player),
                match=Match.objects.get(pk=matchId),
                minute=minute
            )
            return HttpResponse()
        else:
            error_msg = u"Insufficient POST data (need 'player, match and team')"
    return HttpResponseServerError(error_msg)
