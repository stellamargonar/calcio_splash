from collections import OrderedDict
from itertools import chain

from calcio_splash.models import Match, Team, Tournament


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

            if match.team_a is None or match.team_b is None:
                continue

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
        team_list = [
            {
                'name': team_name,
                'points': team.get('points', 0),
                'goals_done': team.get('goals_done', 0),
                'goals_taken': team.get('goals_taken', 0),
                'goals_diff': team.get('goals_done', 0) - team.get('goals_taken', 0),
                'pk': team['pk'],
            }
            for team_name, team in teams.items()
        ]
        sorted_teams = sorted(team_list, key=lambda x: (x['points'], x['goals_diff']), reverse=True)

        group.teams = OrderedDict([(team['name'], team) for team in sorted_teams])
        group.is_beach = False
        return group

    @staticmethod
    def build_beach_group(group):
        teams = dict()
        matches = list()
        for match in group.beach_matches.all().order_by('match_date_time'):
            matches += [match]

            if match.team_a is None or match.team_b is None:
                continue

            team_a = teams.get(match.team_a.name, {})
            team_b = teams.get(match.team_b.name, {})

            if match.is_tie:
                points_a = 1
                points_b = 1
            else:
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
        team_list = [
            {
                'name': team_name,
                'points': team.get('points', 0),
                'pk': team['pk'],
            }
            for team_name, team in teams.items()
        ]
        sorted_teams = sorted(team_list, key=lambda x: -x['points'])
        group.teams = OrderedDict([(team['name'], team) for team in sorted_teams])
        group.is_beach = True
        return group

    @staticmethod
    def _score_from_match(match: Match):
        if not match.ended:
            return 0, 0
        if match.team_a_score == match.team_b_score:
            return 1, 1
        if match.team_a_score > match.team_b_score:
            return 3, 0
        return 0, 3


class MatchHelper:
    @staticmethod
    def build_match(match: Match):
        goals = match.goals.all()
        players_map = dict()

        for goal in goals:
            if goal.player:
                players_map[goal.player.id] = players_map.get(goal.player.id, 0) + 1

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
                        players[key] = {
                            'player': goal.player,
                            'goals': players.get(key, {}).get('goals', 0) + 1,
                            'team': goal.player.teams.filter(year=tournament.edition_year).first(),
                        }

        player_list = [(obj['player'], obj['goals'], obj['team']) for obj in players.values()]
        player_list.sort(key=lambda x: -x[1])
        return player_list


class BracketsHelper:
    @classmethod
    def _add_participant_if_missing(cls, participants: dict, team: Team):
        if not team or team.pk in participants:
            return
        participants[team.pk] = {"id": team.pk, "tournament_id": 0, "name": team.name}

    @classmethod
    def _match_result(cls, match: Match, team: Team):
        if not match.ended:
            return
        winner = match.winner
        if winner == team:
            return "win"
        return "loss"

    @classmethod
    def build_brackets(cls, tournament: Tournament):
        groups = tournament.groups.filter(is_final=True)
        matches = []
        match_games = []
        participants = {}
        rounds = []
        for n_group, group in enumerate(groups):
            rounds.append({"id": n_group, "number": n_group + 1, "stage_id": 0, "group_id": 0})
            is_finalissima_group = n_group == groups.count() - 1

            for n_match, match in enumerate(chain(group.matches.all(), group.beach_matches.all())):
                # [sp] this is a dirty hack to hide a mess we did in 2018: in the F tournament, for some reason
                # we let play the 3rd and the 4th of the two round-robin groups, just because.
                if isinstance(match, Match) and match.pk in {99, 100}:
                    continue
                is_consolation_final = is_finalissima_group and n_match == 0
                cls._add_participant_if_missing(participants, match.team_a)
                cls._add_participant_if_missing(participants, match.team_b)

                status = 0  # waiting
                if match.team_a or match.team_b:
                    status = 1  # waiting
                if match.team_a and match.team_b:
                    status = 2  # ready
                if match.ended:
                    status = 4  # completed

                match_dict = {
                    "id": match.id,
                    "number": n_match + 1,
                    "stage_id": 0,
                    "group_id": 1 if is_consolation_final else 0,
                    "round_id": n_group,  # the JS library sorts by this, so we can't use group.pk :/
                    "round_id_real": group.pk,
                    "status": status,
                    "opponent1": {"id": match.team_a.pk, "result": cls._match_result(match, match.team_a)}
                    if match.team_a
                    else None,
                    "opponent2": {"id": match.team_b.pk, "result": cls._match_result(match, match.team_b)}
                    if match.team_b
                    else None,
                }

                if isinstance(match, Match):
                    started = match.ended or match.score_a > 0 or match.score_b > 0
                    match_dict["child_count"] = 1
                    if started and match.team_a:
                        match_dict["opponent1"]["score"] = match.score_a
                    if started and match.team_b:
                        match_dict["opponent2"]["score"] = match.score_b
                else:
                    started = match.ended or match.team_a_set_1 is not None and match.team_b_set_1 is not None
                    match_dict["child_count"] = 3
                    if started and match.team_a:
                        match_dict["opponent1"]["score"] = "-".join(
                            str(x)
                            for x in [match.team_a_set_1, match.team_a_set_2, match.team_a_set_3]
                            if x is not None
                        )
                    if started and match.team_b:
                        match_dict["opponent2"]["score"] = "-".join(
                            str(x)
                            for x in [match.team_b_set_1, match.team_b_set_2, match.team_b_set_3]
                            if x is not None
                        )

                matches.append(match_dict)

        if not rounds:
            return None

        return {
            "participants": list(participants.values()) or [{}],  # participants must not be empty
            "stages": [
                {
                    "id": 0,
                    "tournament_id": 0,
                    "name": "",
                    "type": "single_elimination",
                    "number": 1,
                    "settings": {
                        "size": len(participants),
                        "seedOrdering": ["natural"],
                        "grandFinal": "single",
                        "consolationFinal": True,
                    },
                }
            ],
            "groups": [{"id": 0, "stage_id": 0, "number": 1}, {"id": 1, "stage_id": 0, "number": 2}],
            "rounds": rounds,
            "matches": matches,
            "matchGames": match_games,
        }
