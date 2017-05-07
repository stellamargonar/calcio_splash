from calcio_splash.models import Group, Match, Team

class GroupHelper:
    @staticmethod
    def build_group(group):
        teams = dict()
        matches = list()
        for match in group.matches.all():
            match, _ = MatchHelper.build_match(match)
            matches += [match]

            team_a = teams.get(match.team_a.name, {})
            team_a['goals_done'] = team_a.get('goals_done', 0) + match.team_a_score
            team_a['goals_taken'] = team_a.get('goals_taken', 0) + match.team_b_score
            team_a['points'] = team_a.get('points', 0) + \
                2 if match.team_a_score > match.team_b_score else \
                1 if match.team_a_score == match.team_b_score else 0
            teams[match.team_a.name] = team_a

            team_b = teams.get(match.team_b.name, {})
            team_b['goals_done'] = team_b.get('goals_done', 0) + match.team_b_score
            team_b['goals_taken']= team_b.get('goals_taken', 0) + match.team_a_score
            team_b['points'] = team_b.get('points', 0) + \
                2 if match.team_b_score > match.team_a_score else \
                1 if match.team_b_score == match.team_a_score else 0
            teams[match.team_b.name] = team_b
        group.group_matches = matches
        # post process teams
        group.teams = {
            team_name: {
                'points': team.get('points', 0),
                'goals_done': team.get('goals_done', 0),
                'goals_taken': team.get('goals_taken', 0),
                'goals_diff': team.get('goals_done', 0) - team.get('goals_taken', 0)
            } for team_name, team in teams.items()
        }

        # TODO sort by points

        return group

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
