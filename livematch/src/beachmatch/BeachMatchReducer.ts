import {BeachMatch, BeachMatchAction} from "./BeachMatchActionsHelper";

export interface BeachMatchState {
    matches: BeachMatch[];
    match: BeachMatch;
}

export function clone<T>(ob: T): T {
    return JSON.parse(JSON.stringify(ob));
}

export class BeachMatchReducer {
    static getInitialState(): BeachMatchState {
        return {
            match: null,
            matches: [],
        };
    }

    static reducer(prevState: BeachMatchState, action: BeachMatchAction): BeachMatchState {
        if (typeof prevState === 'undefined') {
            return BeachMatchReducer.getInitialState();
        }

        switch (action.type) {
            case 'BEACH_MATCH_SET_MATCHES':
                return {
                    ...prevState,
                    matches: action.matches,
                };
            case 'BEACH_MATCH_SET_MATCH':
                return {
                    ...prevState,
                    match: action.match,
                };

            case 'BEACH_MATCH_SCORE': {
                let currentMatch = clone(prevState.match),
                    isA = action.teamId === currentMatch.team_a.pk;

                if (action.set == 1) {
                    currentMatch.team_a_set_1 = currentMatch.team_a_set_1 + (isA ? 1 : 0);
                    currentMatch.team_b_set_1 = currentMatch.team_b_set_1 + (isA ? 0 : 1);
                } else if (action.set == 2) {
                    currentMatch.team_a_set_2 = currentMatch.team_a_set_2 + (isA ? 1 : 0);
                    currentMatch.team_b_set_2 = currentMatch.team_b_set_2 + (isA ? 0 : 1);
                } else {
                    currentMatch.team_a_set_3 = currentMatch.team_a_set_3 + (isA ? 1 : 0);
                    currentMatch.team_b_set_3 = currentMatch.team_b_set_3 + (isA ? 0 : 1);
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

            default:
                return prevState;
        }
    }
}
