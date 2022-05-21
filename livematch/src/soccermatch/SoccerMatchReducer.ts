import {SoccerMatch, SoccerMatchAction} from "./SoccerMatchActionsHelper";

export interface SoccerMatchState {
    matches: SoccerMatch[];
    match: SoccerMatch;
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
                console.log('REDUCER', action);
                return {
                    ...prevState,
                    matches: action.matches,
                };
            case 'SOCCER_MATCH_SET_MATCH':
                console.log('REDUCER', action);
                return {
                    ...prevState,
                    match: action.match,
                };

            default:
                return prevState;
        }
    }
}
