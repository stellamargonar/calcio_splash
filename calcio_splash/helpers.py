from collections import OrderedDict
from datetime import timedelta

from django.db.models import Max, Sum
from django.utils import timezone

from calcio_splash.models import Tournament, Group, Match, Team, BeachMatch


class GroupHelper:
    @staticmethod
    def build_group(group):
        if 'beach' in group.tournament.name.lower():
            return GroupHelper.build_beach_group(group)

        teams = dict()
        matches = list()
        for match in group.matches.all().order_by('match_date_time'):
            match, _ = MatchHelper.build_match(match)
            matches += [match]

            team_a = teams.get(match.team_a.name, {})
            team_a['pk'] = match.team_a.pk
            team_a['goals_done'] = team_a.get('goals_done', 0) + match.team_a_score
            team_a['goals_taken'] = team_a.get('goals_taken', 0) + match.team_b_score

            team_b = teams.get(match.team_b.name, {})
            team_b['pk'] = match.team_b.pk
            team_b['goals_done'] = team_b.get('goals_done', 0) + match.team_b_score
            team_b['goals_taken'] = team_b.get('goals_taken', 0) + match.team_a_score

            points_a, points_b = GroupHelper._score_from_match(match)
            team_a['points'] = team_a.get('points', 0) + points_a
            team_b['points'] = team_b.get('points', 0) + points_b

            teams[match.team_a.name] = team_a
            teams[match.team_b.name] = team_b
        group.group_matches = matches

        # post process teams
        team_list = [{
            'name': team_name,
            'points': team.get('points', 0),
            'goals_done': team.get('goals_done', 0),
            'goals_taken': team.get('goals_taken', 0),
            'goals_diff': team.get('goals_done', 0) - team.get('goals_taken', 0),
            'pk': team['pk'],
        } for team_name, team in teams.items()]
        sorted_teams = sorted(team_list, key=lambda x: -x['points'])

        group.teams = OrderedDict([(team['name'], team) for team in sorted_teams])
        group.is_beach = False
        return group

    @staticmethod
    def build_beach_group(group):
        teams = dict()
        matches = list()
        for match in group.beach_matches.all().order_by('match_date_time'):
            matches += [match]

            team_a = teams.get(match.team_a.name, {})
            team_b = teams.get(match.team_b.name, {})

            points_a = 3 if match.winner == match.team_a else 0
            points_b = 3 if match.winner == match.team_b else 0

            team_a['points'] = team_a.get('points', 0) + points_a
            team_a['pk'] = match.team_a.pk
            team_b['points'] = team_b.get('points', 0) + points_b
            team_b['pk'] = match.team_b.pk

            teams[match.team_a.name] = team_a
            teams[match.team_b.name] = team_b

        group.group_matches = matches

        # post process teams
        team_list = [{
            'name': team_name,
            'points': team.get('points', 0),
            'pk': team['pk'],
        } for team_name, team in teams.items()]
        sorted_teams = sorted(team_list, key=lambda x: -x['points'])
        group.teams = OrderedDict([(team['name'], team) for team in sorted_teams])
        group.is_beach = True
        return group

    @staticmethod
    def _score_from_match(match):
        if match.end_time is None:
            return 0, 0
        if match.team_a_score == match.team_b_score:
            return 1, 1
        if match.team_a_score > match.team_b_score:
            return 3, 0
        return 0, 3

    @staticmethod
    def generate_new_groups_for_calcio(tournament: Tournament):
        if any(match.end_time is None for match in Match.objects.filter(group__tournament=tournament)):
            raise Exception('Some match are not closed')

        gironi = [GroupHelper.build_group(group) for group in tournament.groups.all() if not group.is_final]
        quarti = [group for group in tournament.groups.all() if group.is_final and group.name.startswith('Quarti')]
        semi = [group for group in tournament.groups.all() if group.is_final and group.name.startswith('Semi')]
        finali = [group for group in tournament.groups.all() if group.is_final and group.name.startswith('Finali')]

        gironi_as_list = [list(girone.teams.values()) for girone in gironi]

        def _get_team(team: dict):
            return Team.objects.get(pk=team['pk'])

        def _create_match(group, team_a, team_b, finale=False):
            max_time = Match.objects.filter(group__tournament__edition_year=tournament.edition_year).aggregate(Max('match_date_time'))
            next_match_time = max_time['match_date_time__max'] + timedelta(minutes=20 if finale is False else 30)
            Match.objects.create(group=group, team_a=team_a, team_b=team_b, match_date_time=next_match_time)

        if len(quarti) == 0 and tournament.name.startswith('M'):
            # solo i maschili hanno i quarti
            assert len(gironi) == 4, f"I gironi di {tournament.name} sono {len(gironi)} ma ne servono 4"
            group = Group.objects.create(tournament=tournament, name=f'Quarti {tournament.name}', is_final=True)

            _create_match(group, _get_team(gironi_as_list[0][0]), _get_team(gironi_as_list[1][1]))
            _create_match(group, _get_team(gironi_as_list[0][1]), _get_team(gironi_as_list[1][0]))
            _create_match(group, _get_team(gironi_as_list[2][0]), _get_team(gironi_as_list[3][1]))
            _create_match(group, _get_team(gironi_as_list[2][1]), _get_team(gironi_as_list[3][0]))
            return

        if len(semi) == 0:
            group = Group.objects.create(tournament=tournament, name=f'Semifinali {tournament.name}', is_final=True)

            if tournament.name.startswith('M'):
                quarti_matches = quarti[0].matches
                _create_match(group, quarti_matches[0].winner, quarti_matches[1].winner)
                _create_match(group, quarti_matches[2].winner, quarti_matches[3].winner)

            else:
                if len(gironi) == 1:
                    # un unico girone: 1 vs 3 e 2 vs 4
                    _create_match(group, _get_team(gironi_as_list[0][0]), _get_team(gironi_as_list[0][2]))
                    _create_match(group, _get_team(gironi_as_list[0][1]), _get_team(gironi_as_list[0][3]))

                else:
                    # 2 gironi femminili -> come le maschili
                    _create_match(group, _get_team(gironi_as_list[0][0]), _get_team(gironi_as_list[1][1]))
                    _create_match(group, _get_team(gironi_as_list[0][1]), _get_team(gironi_as_list[1][0]))
            return

        if len(finali) == 0:
            semi_matches = semi[0].matches
            group = Group.objects.create(tournament=tournament, name=f'Finali {tournament.name}', is_final=True)
            _create_match(group, semi_matches[0].winner, semi_matches[1].winner)
            _create_match(group, semi_matches[0].loser, semi_matches[1].loser)

        return

    @staticmethod
    def generate_new_groups_for_beach(tournament: Tournament):
        gironi = [GroupHelper.build_beach_group(group) for group in tournament.groups.all() if not group.is_final]
        quarti = [group for group in tournament.groups.all() if group.is_final and group.name.startswith('Quarti')]
        semi = [group for group in tournament.groups.all() if group.is_final and group.name.startswith('Semi')]
        finali = [group for group in tournament.groups.all() if group.is_final and group.name.startswith('Finali')]

        def _create_match(group, team_a, team_b, finale=False):
            max_time = BeachMatch.objects.filter(group__tournament__edition_year=tournament.edition_year).aggregate(Max('match_date_time'))
            next_match_time = max_time['match_date_time__max'] + timedelta(minutes=20 if finale is False else 30)
            BeachMatch.objects.create(group=group, team_a=team_a, team_b=team_b, match_date_time=next_match_time)

        def _get_team(team: dict):
            return Team.objects.get(pk=team['pk'])

        if len(quarti) == 0:
            assert len(gironi) == 3, "Mi servono 3 gironi di beach"

            # calcola il peggior terzo, voglio ottenere i gironi ordinati in modo che i primi 2 abbiano 3 squadre, e il terzo 2
            thirds = []
            for i, team in enumerate([list(girone.teams.values())[2] for girone in gironi]):
                breakpoint()
                points_a = BeachMatch.objects.filter(team_a__pk=team['pk']).aggregate(Sum('team_a_set_1'), Sum('team_a_set_2'), Sum('team_a_set_3'))
                points_b = BeachMatch.objects.filter(team_b__pk=team['pk']).aggregate(Sum('team_b_set_1'), Sum('team_b_set_2'), Sum('team_b_set_3'))
                points = sum([points_a.get(f'team_a_set_{k}__sum') or 0 for k in range(1, 4)] + [points_b.get(f'team_b_set_{k}__sum') or 0 for k in range(1, 4)])
                thirds.append((i, points))
            thirds.sort(key=lambda x: -x[1])
            gironi_as_list = [list(gironi[key].teams.values())for (key, _) in thirds]

            group = Group.objects.create(tournament=tournament, name=f'Quarti Beach', is_final=True)
            _create_match(group, _get_team(gironi_as_list[0][0]), _get_team(gironi_as_list[1][2]))
            _create_match(group, _get_team(gironi_as_list[1][0]), _get_team(gironi_as_list[2][1]))
            _create_match(group, _get_team(gironi_as_list[2][0]), _get_team(gironi_as_list[0][2]))
            _create_match(group, _get_team(gironi_as_list[2][1]), _get_team(gironi_as_list[0][1]))
            return

        if len(semi) == 0:
            group = Group.objects.create(tournament=tournament, name=f'Semifinali Beach', is_final=True)
            quarti_matches = quarti[0].beach_matches
            _create_match(group, quarti_matches[0].winner, quarti_matches[1].winner)
            _create_match(group, quarti_matches[2].winner, quarti_matches[3].winner)
            return

        if len(finali) == 0:
            semi_matches = semi[0].beach_matches
            group = Group.objects.create(tournament=tournament, name=f'Finali Beach', is_final=True)
            _create_match(group, semi_matches[0].winner, semi_matches[1].winner)
            _create_match(group, semi_matches[0].loser, semi_matches[1].loser)

        return


class MatchHelper:
    @staticmethod
    def build_match(match):
        goals = match.goals.all()

        # compute score
        team_a_score = 0
        team_b_score = 0

        players_map = dict()

        for goal in goals:
            if goal.team == match.team_a:
                team_a_score += 1
            if goal.team == match.team_b:
                team_b_score += 1
            if goal.player:
                players_map[goal.player.id] = players_map.get(goal.player.id, 0) + 1

        match.goals.set(goals)
        match.team_a_score = team_a_score
        match.team_b_score = team_b_score

        return match, players_map


class BeachMatchHelper:
    @staticmethod
    def build_match(match):
        current_set = None

        if match.team_a_set_1 is not None or match.team_b_set_1 is not None:
            match.team_a_set_1 = match.team_a_set_1 or 0
            match.team_b_set_1 = match.team_b_set_1 or 0
            current_set = 1

        if match.team_a_set_2 is not None or match.team_b_set_2 is not None:
            match.team_a_set_2 = match.team_a_set_2 or 0
            match.team_b_set_2 = match.team_b_set_2 or 0
            current_set = 2

        if match.team_a_set_3 is not None or match.team_b_set_3 is not None:
            match.team_a_set_3 = match.team_a_set_3 or 0
            match.team_b_set_3 = match.team_b_set_3 or 0
            current_set = 3

        match.save()
        return match, current_set


class AlboDoroHelper:
    @staticmethod
    def build_albo(tournament):
        tournament.players = AlboDoroHelper.players_by_scores(tournament)
        return tournament

    @staticmethod
    def players_by_scores(tournament):
        players = dict()
        for group in tournament.groups.all():
            for match in group.matches.all():
                for goal in match.goals.all():
                    if goal.player:
                        key = goal.player.pk
                        players[key] = {'player': goal.player, 'goals': players.get(key, {}).get('goals', 0) + 1}

        player_list = [(obj['player'], obj['goals']) for obj in players.values()]
        player_list.sort(key=lambda x: -x[1])
        return player_list
