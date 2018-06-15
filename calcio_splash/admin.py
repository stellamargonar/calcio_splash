from django import forms
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.core import serializers
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponseServerError, HttpResponseRedirect

from datetime import datetime

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
            url(r'match_goals/(?P<id>\d+)/undo$', delete_last_goal),
            url(r'match_goals/(?P<id>\d+)/start$', start_match),
            url(r'match_goals/(?P<id>\d+)/end$', end_match),
            url(r'match_goals/(?P<id>\d+)/endprimotempo$', end_primo_tempo),
            url(r'match_goals/(?P<id>\d+)/startsecondotempo$', start_secondo_tempo),
            url(r'match_goals/(?P<id>\d+)/reset$', reset_match),
        ]
        return urls


admin_site = CalcioSplashAdminSite()


class TeamYearFilter(SimpleListFilter):
    title = 'Filtra per anno'
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        years = Team.objects.values('year').distinct()
        return [
            (year['year'], year['year']) for year in years
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(year=self.value())
        return queryset


class TeamAdmin(admin.ModelAdmin):
    inlines = (PlayerAdminInline,)
    list_display = ['name']
    list_filter = (TeamYearFilter,)


admin_site.register(Team, TeamAdmin)


class PlayerAdmin(admin.ModelAdmin):
    list_display = ['surname', 'name']


admin_site.register(Player, PlayerAdmin)


class MatchEndedListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'terminata'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'ended'

    def lookups(self, request, model_admin):
        return (
            ('ended', 'Finita'),
            ('playing', 'In Corso'),
            ('unstarted', 'Non Iniziata'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'ended':
            return queryset.filter(end_time__lte=datetime.now())
        if self.value() == 'playing':
            return queryset.filter(start_time__lte=datetime.now(), end_time=None)
        if self.value() == 'unstarted':
            return queryset.filter(start_time=None)


class MatchTournamentListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'torneo'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'tournament'

    def lookups(self, request, model_admin):
        return (
            ('maschile', 'Maschile'),
            ('femminile', 'Femminile'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'maschile':
            return queryset.filter(group__tournament__name='Maschile')
        if self.value() == 'femminile':
            return queryset.filter(group__tournament__name='Femminile')


class MatchAdmin(admin.ModelAdmin):
    list_display = ['get_datetime', 'get_tournament', 'get_group', 'get_team_a', 'get_team_b', 'get_score']
    form = MatchForm
    actions = ['go_to_match_page']
    list_filter = ('group', MatchEndedListFilter, MatchTournamentListFilter)
    search_fields = ['team_a__name', 'team_b__name']

    def get_tournament(self, obj):
        return obj.group.tournament.name

    def get_group(self, obj):
        return obj.group.name

    def get_team_a(self, obj):
        return obj.team_a.name

    def get_team_b(self, obj):
        return obj.team_b.name

    def get_score(self, obj):
        match, _ = MatchHelper.build_match(obj)
        if match.end_time is None:
            return '-'
        return '{} - {}'.format(match.team_a_score, match.team_b_score)

    def get_datetime(self, obj):
        return obj.match_date_time.strftime('%d/%m %H:%M')

    def go_to_match_page(modeladmin, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect("admin/calcio_splash/match_goals/" + selected[0])

    get_group.short_description = 'Group'
    get_team_a.short_description = 'Team A'
    get_team_b.short_description = 'Team B'
    get_score.short_description = 'Risultato'
    get_tournament.short_description = 'Torneo'
    go_to_match_page.short_description = 'Start Match'
    get_group.admin_order_field = 'group'
    get_datetime.admin_order_field = 'match_date_time'


admin_site.register(Match, MatchAdmin)


class GroupAdmin(admin.ModelAdmin):
    list_display = ['name']


admin_site.register(Group, GroupAdmin)


class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'edition_year']


admin_site.register(Tournament, TournamentAdmin)


class GoalGroupListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'girone'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'group'

    def lookups(self, request, model_admin):
        return [
            (group.name, group.name)
            for group in Group.objects.all()
        ]

    def queryset(self, request, queryset):
        return queryset.filter(match__group__name=self.value())


class GoalAdmin(admin.ModelAdmin):
    list_display = ['get_match', 'get_team', 'get_player']
    list_filter = ('match', 'player')

    def get_match(self, obj):
        return obj.match.team_a.name + obj.match.team_b.name

    def get_team(self, obj):
        return obj.team.name

    def get_player(self, obj):
        if obj.player:
            return obj.player.name
        return ''


admin_site.register(Goal, GoalAdmin)


class MatchGoalAdmin(TemplateView, admin.ModelAdmin):
    template_name = 'admin/match_goal.html'

    def get_context_data(self, id, **kwargs):
        context = super().get_context_data(**kwargs)
        match = Match.objects.get(id=id)

        context['match'], context['player_goals'] = MatchHelper.build_match(match)
        return context


def create_goal(request, id):
    error_response = _validate_post_request(request, ['team', 'minute'])
    if error_response:
        return error_response
    post = request.POST.copy()

    team = post['team']
    player = post.get('player')
    minute = post['minute']

    match = Match.objects.get(pk=id)
    if match.start_secondo_tempo is not None:
        minute = int(minute) + (((match.end_primo_tempo - match.start_time).seconds // 60) % 60)

    matchId = id
    new_goal = Goal.objects.create(
        team=Team.objects.get(pk=team),
        player=Player.objects.get(pk=player) if player else None,
        match=Match.objects.get(pk=matchId),
        minute=minute
    )

    # return the new match score
    match, player_map = MatchHelper.build_match(Match.objects.get(pk=matchId))
    return JsonResponse({
        'team_a_score': match.team_a_score,
        'team_b_score': match.team_b_score,
        'playerMap': player_map
    }, safe=False)


def delete_last_goal(request, id):
    error_response = _validate_post_request(request, ['team'])
    if error_response:
        return error_response
    post = request.POST.copy()

    team = post['team']
    player = post.get('player')
    matchId = id
    goals = Goal.objects.filter(
        team=Team.objects.get(pk=team),
        player=Player.objects.get(pk=player) if player else None,
        match=Match.objects.get(pk=matchId)
    ).order_by('-minute')

    if len(goals) == 0:
        return HttpResponseServerError(u'No goal find for this player')

    goals[0].delete()

    # return the new match score
    match, player_map = MatchHelper.build_match(Match.objects.get(pk=matchId))
    return JsonResponse({
        'team_a_score': match.team_a_score,
        'team_b_score': match.team_b_score,
        'playerMap': player_map
    })


def reset_match(request, id):
    post = request.POST.copy()
    Match.objects.filter(pk=id).update(start_time=None, end_time=None, end_primo_tempo=None, start_secondo_tempo=None)
    Goal.objects.filter(match_id=id).delete()
    return JsonResponse({"status": "ok"})


def start_match(request, id):
    error_response = _validate_post_request(request, ['time'])
    if error_response:
        return error_response

    post = request.POST.copy()
    time = datetime.fromtimestamp(int(post['time']) / 1000)
    matchId = id
    Match.objects.filter(pk=matchId).update(start_time=time)
    return JsonResponse({
        'time': post['time']
    })


def end_match(request, id):
    error_response = _validate_post_request(request, ['time'])
    if error_response:
        return error_response

    post = request.POST.copy()
    time = datetime.fromtimestamp(int(post['time']) / 1000)
    matchId = id
    Match.objects.filter(pk=matchId).update(end_time=time)
    return JsonResponse({
        'time': post['time']
    })


def end_primo_tempo(request, id):
    error_response = _validate_post_request(request, ['time'])
    if error_response:
        return error_response

    post = request.POST.copy()
    time = datetime.fromtimestamp(int(post['time']) / 1000)
    matchId = id
    Match.objects.filter(pk=matchId).update(end_primo_tempo=time)
    return JsonResponse({
        'time': post['time']
    })


def start_secondo_tempo(request, id):
    error_response = _validate_post_request(request, ['time'])
    if error_response:
        return error_response

    post = request.POST.copy()
    time = datetime.fromtimestamp(int(post['time']) / 1000)
    matchId = id
    Match.objects.filter(pk=matchId).update(start_secondo_tempo=time)
    return JsonResponse({
        'time': post['time']
    })


def _validate_post_request(request, required_params):
    error_msg = u"No POST data sent."
    if not (request.method == "POST"):
        return HttpResponseServerError(error_msg)

    post = request.POST.copy()
    if any(not (post.get(param)) for param in required_params):
        return HttpResponseServerError(u"Insufficient POST data (need {}})".format(required_params))
    return None
