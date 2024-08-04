from datetime import datetime, timedelta

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.utils import timezone

from calcio_splash.forms import BeachMatchForm, MatchForm, PlayerAdminInline
from calcio_splash.helpers import BeachMatchHelper, MatchHelper
from calcio_splash.models import BeachMatch, Goal, Group, Match, Player, Team, Tournament


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
                'query_string': cl.get_query_string(
                    {
                        self.parameter_name: lookup,
                    },
                    [],
                ),
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


admin_site = admin.AdminSite()
admin_site.register(User, UserAdmin)


class TeamYearFilter(AbstractListFilterWithDefault):
    title = 'Filtra per anno'
    default = timezone.now().year
    default_name = str(timezone.now().year)
    parameter_name = 'year'
    _zero_value = '*'

    def lookups(self, request, model_admin):
        years = Team.objects.values('year').distinct()
        return [(year['year'], year['year']) for year in years]

    def queryset_filter(self, request, queryset, value):
        return queryset.filter(year=value)


class TeamAdmin(admin.ModelAdmin):
    inlines = (PlayerAdminInline,)
    list_display = ['name', 'year', 'gender', 'nr_players']
    list_filter = (TeamYearFilter, 'gender')
    search_fields = ('name',)

    def nr_players(self, instance) -> int:
        return instance.player.count()

    nr_players.short_description = '# Players'


admin_site.register(Team, TeamAdmin)


class PlayerAdmin(admin.ModelAdmin):
    list_display = ['surname', 'name', 'nickname', 'date_of_birth']
    ordering = ('name', 'surname', 'nickname', 'date_of_birth')
    search_fields = ('name', 'surname', 'nickname')
    filter_horizontal = ('teams',)


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
            for day in Match.objects.filter(match_date_time__year=timezone.now().year)
            .exclude(match_date_time__date=self.default)
            .dates('match_date_time', 'day')
            .all()
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
            for year in Match.objects.exclude(match_date_time__year=timezone.now().year)
            .dates('match_date_time', 'year')
            .all()
        ]

    def queryset_filter(self, request, queryset, value):
        return queryset.filter(match_date_time__year=value)


class MatchAdmin(admin.ModelAdmin):
    list_display = [
        'get_datetime',
        'get_team_a',
        'get_team_b',
        'get_score',
        'get_tournament',
        'get_group',
        'brackets_offset',
    ]
    form = MatchForm
    actions = ['go_to_match_page']
    list_filter = (
        MatchDateListFilter,
        MatchEndedListFilter,
        MatchTournamentListFilter,
        MatchYearListFilter,
        'group',
    )
    search_fields = ['team_a__name', 'team_b__name']
    ordering = [
        'match_date_time',
    ]
    raw_id_fields = [
        'team_a',
        'team_b',
    ]

    def get_tournament(self, obj):
        return '{} ({})'.format(obj.group.tournament.name, obj.group.tournament.edition_year)

    def get_group(self, obj):
        return obj.group.name

    def get_team_a(self, obj):
        return obj.team_a.name if obj.team_a else '-'

    def get_team_b(self, obj):
        return obj.team_b.name if obj.team_b else '-'

    def get_score(self, obj):
        match, _ = MatchHelper.build_match(obj)
        if not match.ended:
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


class BeachMatchAdmin(MatchAdmin):
    form = BeachMatchForm

    def get_score(self, obj):
        match, current_set = BeachMatchHelper.build_match(obj)
        if current_set is None:
            return '-'

        field_template = 'team_{}_set_{}'
        scores = []
        for set_nr in range(1, current_set + 1):
            scores.append(
                '{} - {}'.format(
                    getattr(match, field_template.format('a', set_nr)),
                    getattr(match, field_template.format('b', set_nr)),
                )
            )
        return ' | '.join(scores)

    def go_to_match_page(modeladmin, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect("admin/calcio_splash/match_beach/" + selected[0])


admin_site.register(BeachMatch, BeachMatchAdmin)


class GroupYearListFilter(AbstractListFilterWithDefault):
    title = 'anno'
    parameter_name = 'edition_year'
    default = timezone.now().year
    default_name = str(timezone.now().year)
    _zero_value = '*'

    def lookup_values(self, request, model_admin):
        return [(year, year) for year in set(Tournament.objects.values_list('edition_year', flat=True))]

    def queryset_filter(self, request, queryset, value):
        return queryset.filter(tournament__edition_year=value)


class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'ordering', 'get_tournament']
    list_filter = (GroupYearListFilter,)

    def get_tournament(self, obj):
        return '{} ({})'.format(obj.tournament.name, obj.tournament.edition_year)

    get_tournament.short_description = 'Torneo'


admin_site.register(Group, GroupAdmin)


class TournamentAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'edition_year',
        'name',
    ]
    list_filter = ('edition_year',)
    raw_id_fields = ('team_1', 'team_2', 'team_3', 'goalkeeper', 'top_scorer')


admin_site.register(Tournament, TournamentAdmin)


class GoalGroupListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'girone'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'group'

    def lookups(self, request, model_admin):
        return [(group.name, group.name) for group in Group.objects.all()]

    def queryset(self, request, queryset):
        return queryset.filter(match__group__name=self.value())


class GoalAdmin(admin.ModelAdmin):
    list_display = ['get_match', 'get_team', 'get_player']
    search_fields = ('team__name', 'player__name', 'player__surname')

    def get_match(self, obj):
        return obj.match.team_a.name + obj.match.team_b.name

    def get_team(self, obj):
        return obj.team.name

    def get_player(self, obj):
        if obj.player:
            return obj.player.name
        return ''


admin_site.register(Goal, GoalAdmin)
