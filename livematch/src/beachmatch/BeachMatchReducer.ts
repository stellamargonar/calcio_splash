import {BeachMatch, BeachMatchAction} from "./BeachMatchActionsHelper";

export interface BeachMatchState {
    matches: BeachMatch[];
    match: BeachMatch;
    isLoading: boolean;
}

export function clone<T>(ob: T): T {
    return JSON.parse(JSON.stringify(ob));
}

export class BeachMatchReducer {
    static getInitialState(): BeachMatchState {
        return {
            match: null,
            matches: [],
            isLoading: false,
        };
    }

    static reducer(prevState: BeachMatchState, action: BeachMatchAction): BeachMatchState {
        if (typeof prevState === 'undefined') {
            return BeachMatchReducer.getInitialState();
        }

        switch (action.type) {
            case 'BEACH_MATCH_SET_MATCHES':
                let currentMatches = action.matches;
                if (!action.showEnded) {
                    currentMatches = currentMatches.filter((match) => !match.ended);
                }

                return {
                    ...prevState,
                    matches: currentMatches,
                };
            case 'BEACH_MATCH_SET_MATCH':
                return {
                    ...prevState,
                    match: action.match,
                };

            case 'BEACH_MATCH_SCORE': {
                let currentMatch = clone(prevState.match),
                    isA = action.teamId === currentMatch.team_a.pk,
                    diff = (action.remove) ? -1 : 1;

                if (action.set == 1) {
                    currentMatch.team_a_set_1 = currentMatch.team_a_set_1 + (isA ? diff : 0);
                    currentMatch.team_b_set_1 = currentMatch.team_b_set_1 + (isA ? 0 : diff);
                } else if (action.set == 2) {
                    currentMatch.team_a_set_2 = currentMatch.team_a_set_2 + (isA ? diff : 0);
                    currentMatch.team_b_set_2 = currentMatch.team_b_set_2 + (isA ? 0 : diff);
                } else {
                    currentMatch.team_a_set_3 = currentMatch.team_a_set_3 + (isA ? diff : 0);
                    currentMatch.team_b_set_3 = currentMatch.team_b_set_3 + (isA ? 0 : diff);
                }

                return {
                    ...prevState,
                    match: currentMatch,
                }
            }
            case 'BEACH_MATCH_RESET': {
                let currentMatch = clone(prevState.match);
                currentMatch.team_a_set_1 = 0;
                currentMatch.team_b_set_1 = 0;
                currentMatch.team_a_set_2 = 0;
                currentMatch.team_b_set_2 = 0;
                currentMatch.team_a_set_3 = 0;
                currentMatch.team_b_set_3 = 0;

                return {
                    ...prevState,
                    match: currentMatch,
                }
            }
            case 'BEACH_MATCH_LOCK': {
                let currentMatches = clone(prevState.matches).map((match) => {
                    if (match.pk == action.matchId) {
                        match.ended = true;
                    }
                    return match;
                });
                let currentMatch = clone(prevState.match);
                if (currentMatch != null && currentMatch.pk == action.matchId) {
                    currentMatch.ended = true;
                }
                return {
                    ...prevState,
                    matches: currentMatches,
                    match: currentMatch
                }
            }
            case 'BEACH_MATCH_UNLOCK': {
                let currentMatches = clone(prevState.matches).map((match) => {
                    if (match.pk == action.matchId) {
                        match.ended = false;
                    }
                    return match;
                });
                let currentMatch = clone(prevState.match);
                if (currentMatch != null && currentMatch.pk == action.matchId) {
                    currentMatch.ended = false;
                }

                return {
                    ...prevState,
                    matches: currentMatches,
                    match: currentMatch,
                }
            }
            case 'BEACH_MATCH_SET_LOADING': {
                return {
                    ...prevState,
                    isLoading: action.isLoading,
                }
            }
            default:
                return prevState;
        }
    }
}
