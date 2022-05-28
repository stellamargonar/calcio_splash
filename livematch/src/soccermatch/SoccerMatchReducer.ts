import {SoccerMatch, SoccerMatchAction} from "./SoccerMatchActionsHelper";

export interface SoccerMatchState {
    matches: SoccerMatch[];
    match: SoccerMatch;
}

export function clone<T>(ob: T): T {
    return JSON.parse(JSON.stringify(ob));
}

export class SoccerMatchReducer {
    static getInitialState(): SoccerMatchState {
        return {
            match: null,
            matches: [],
        };
    }

    static reducer(prevState: SoccerMatchState, action: SoccerMatchAction): SoccerMatchState {
        if (typeof prevState === 'undefined') {
            return SoccerMatchReducer.getInitialState();
        }

        switch (action.type) {
            case 'SOCCER_MATCH_SET_MATCHES':
                return {
                    ...prevState,
                    matches: action.matches,
                };
            case 'SOCCER_MATCH_SET_MATCH':
                return {
                    ...prevState,
                    match: action.match,
                };

            case 'SOCCER_MATCH_SCORE': {
                let currentMatch = clone(prevState.match),
                    isA = action.teamId === currentMatch.team_a.pk,
                    team = isA ? currentMatch.team_a : currentMatch.team_b;

                currentMatch.score_a = currentMatch.score_a + (isA ? 1 : 0);
                currentMatch.score_b = currentMatch.score_b + (isA ? 0 : 1);

                let player = null;
                if (action.playerId != null) {
                    player = team.players.find((p) => p.pk === action.playerId);
                    player.score += 1;
                }

                return {
                    ...prevState,
                    match: currentMatch,
                }
            }
            case 'SOCCER_MATCH_RESET': {
                let currentMatch = clone(prevState.match);
                currentMatch.score_a = 0;
                currentMatch.score_b = 0;

                for (let player of currentMatch.team_a.players) {
                    player.score = 0;
                }
                for (let player of currentMatch.team_b.players) {
                    player.score = 0;
                }

                return {
                    ...prevState,
                    match: currentMatch,
                }
            }
            case 'SOCCER_MATCH_LOCK': {
                let currentMatches =  clone(prevState.matches).map((match) => {
                    if (match.pk == action.matchId) {
                        match.ended = true;
                    }
                    return match;
                });
                return {
                    ...prevState,
                    matches: currentMatches,
                }
            }
            case 'SOCCER_MATCH_UNLOCK': {
                let currentMatches =  clone(prevState.matches).map((match) => {
                    if (match.pk == action.matchId) {
                        match.ended = false;
                    }
                    return match;
                });

                return {
                    ...prevState,
                    matches: currentMatches,
                }
            }
            default:
                return prevState;
        }
    }
}
