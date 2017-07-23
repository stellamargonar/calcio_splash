from calcio_splash.models import Group, Match, Team
from collections import OrderedDict

class GroupHelper:
    @staticmethod
    def build_group(group):
        teams = dict()
        matches = list()
        for match in group.matches.all().order_by('match_date_time'):
            match, _ = MatchHelper.build_match(match)
            matches += [match]

            team_a = teams.get(match.team_a.name, {})
            team_a['goals_done'] = team_a.get('goals_done', 0) + match.team_a_score
            team_a['goals_taken'] = team_a.get('goals_taken', 0) + match.team_b_score

            team_b = teams.get(match.team_b.name, {})
            team_b['goals_done'] = team_b.get('goals_done', 0) + match.team_b_score
            team_b['goals_taken']= team_b.get('goals_taken', 0) + match.team_a_score

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
            'goals_diff': team.get('goals_done', 0) - team.get('goals_taken', 0)
        } for team_name, team in teams.items()]
        sorted_teams = sorted(team_list, key=lambda x: -x['points'])

        group.teams = OrderedDict([(team['name'], team) for team in sorted_teams])
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

            players_map[goal.player.id] = players_map.get(goal.player.id, 0) + 1

        match.goals = goals
        match.team_a_score = team_a_score
        match.team_b_score = team_b_score

        return match, players_map


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
                    players[goal.player] = players.get(goal.player, 0) + 1

        player_list = [(player, goals) for player, goals in players.items()]
        player_list.sort(key=lambda x: -x[1])
        print(player_list)
        return player_list
