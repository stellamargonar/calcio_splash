import pytz
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils import timezone
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponseServerError, HttpResponseRedirect

from datetime import datetime, timedelta

from pytz import tzinfo

from calcio_splash.models import Goal, Group, Match, Player, Team, Tournament
from calcio_splash.helpers import MatchHelper
from calcio_splash.forms import MatchForm, PlayerAdminInline


class AbstractListFilterWithDefault(admin.SimpleListFilter):
    default = None
    default_name = None
    parameter_name = None
    title = None
    _zero_value = None

    def lookup_values(self, request, model_admin):
        raise NotImplementedError

    def queryset_filter(self, request, queryset, value):
        raise NotImplementedError

    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def lookups(self, request, model_admin):
        return [(self._zero_value, 'Tutti'), (None, self.default_name)] + self.lookup_values(request, model_admin)

    def queryset(self, request, queryset):
        value_to_filter = self.value()

        if value_to_filter is None:
            value_to_filter = self.default
        elif value_to_filter == self._zero_value:
            return queryset

        return self.queryset_filter(request, queryset, value_to_filter)


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
    ordering = ('name', 'surname')


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
            return queryset.filter(end_time__lte=timezone.now())
        if self.value() == 'playing':
            return queryset.filter(start_time__lte=timezone.now(), end_time__isnull=True)
        if self.value() == 'unstarted':
            return queryset.filter(start_time__isnull=True)


class MatchTournamentListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'torneo'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'tournament'

    def lookups(self, request, model_admin):
        return [
            (tournament.pk, '{} {}'.format(tournament.edition_year, tournament.name))
            for tournament in Tournament.objects.all().order_by('-edition_year')
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(group__tournament=self.value())


class MatchDateListFilter(AbstractListFilterWithDefault):
    title = 'giorno'
    parameter_name = 'day'
    _zero_value = '*'

    @property
    def default(self):
        return datetime.strftime(timezone.now(), '%Y-%m-%d')

    @property
    def default_name(self):
        return datetime.strftime(timezone.now(), '%d/%m')

    def lookup_values(self, request, model_admin):
        return [
            (datetime.strftime(day, '%Y-%m-%d'), datetime.strftime(day, '%d/%m'))
            for day in Match.objects
                            .filter(match_date_time__year=timezone.now().year)
                            .exclude(match_date_time__date=self.default)
                            .dates('match_date_time', 'day').all()
        ]

    def queryset_filter(self, request, queryset, value):
        return queryset.filter(match_date_time__date=value)


class MatchYearListFilter(AbstractListFilterWithDefault):
    title = 'anno'
    parameter_name = 'year'
    default = timezone.now().year
    default_name = str(timezone.now().year)
    _zero_value = '*'

    def lookup_values(self, request, model_admin):
        return [
            (year.year, datetime.strftime(year, '%Y'))
            for year in
            Match.objects.exclude(match_date_time__year=timezone.now().year).dates('match_date_time', 'year').all()
        ]

    def queryset_filter(self, request, queryset, value):
        return queryset.filter(match_date_time__year=value)


class MatchAdmin(admin.ModelAdmin):
    list_display = ['get_datetime', 'get_team_a', 'get_team_b', 'get_score', 'get_tournament', 'get_group', ]
    form = MatchForm
    actions = ['go_to_match_page']
    list_filter = (MatchDateListFilter, MatchEndedListFilter, 'group', MatchTournamentListFilter, MatchYearListFilter)
    search_fields = ['team_a__name', 'team_b__name']
    ordering = ['match_date_time', ]

    def get_tournament(self, obj):
        return '{} ({})'.format(obj.group.tournament.name, obj.group.tournament.edition_year)

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
        return (obj.match_date_time + timedelta(hours=2)).strftime('%d/%m %H:%M')

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
    list_display = ['name', 'get_tournament']

    def get_tournament(self, obj):
        return '{} ({})'.format(obj.tournament.name, obj.tournament.edition_year)

    get_tournament.short_description = 'Torneo'


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
        team_a = context['match'].team_a
        team_b = context['match'].team_b

        context['players_a'] = Player.objects.filter(teams=team_a)
        context['players_b'] = Player.objects.filter(teams=team_b)
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
