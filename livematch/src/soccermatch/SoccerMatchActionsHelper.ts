import jQuery from 'jquery';
import {Store} from "@reduxjs/toolkit";
import {boundMethod} from 'autobind-decorator';
import {createSingleton} from "../utils/SingletonProvider";

export interface Player {
    pk: string;
    name: string;
    score: number;
}

export interface Team {
    pk: string;
    name: string;
    players: Player[];
}

export interface SoccerMatch {
  pk: string;
  team_a: Team;
  team_b: Team;
  score_a: number;
  score_b: number;
}

export type SoccerMatchAction =
    | {type: 'SOCCER_MATCH_SET_MATCHES', matches: SoccerMatch[]}
    | {type: 'SOCCER_MATCH_SET_MATCH', match: SoccerMatch}
    | {type: 'SOCCER_MATCH_SCORE', matchId: string, teamId: string, playerId?: string, remove?: boolean}
    | {type: 'SOCCER_MATCH_RESET', matchId: string};


export class SoccerMatchActionsHelper {
    private store: Store;

    public setStore(store: Store): void {
        this.store = store;
    }

    @boundMethod
    public fetchMatches(): void {
        jQuery.ajax('/api/livematch/')
            .then((response ) => this.dispatch({type: 'SOCCER_MATCH_SET_MATCHES', matches: response}));
    }

    @boundMethod
    public fetchMatch(matchId: string): void {
        jQuery.ajax('/api/livematch/' + matchId)
            .then((response ) => this.dispatch({type: 'SOCCER_MATCH_SET_MATCH', match: response}));
    }

    @boundMethod
    public score(matchId: string, teamId: string, playerId?: string, remove?: boolean): void {
        this.dispatch({type: 'SOCCER_MATCH_SCORE', matchId, teamId, playerId, remove});
        jQuery.ajax('/api/livematch/' + matchId + '/score/', {
            method: 'POST',
            data: JSON.stringify({teamId, playerId, remove}),
            contentType: 'application/json'
        }).then((response) => this.dispatch({type: 'SOCCER_MATCH_SET_MATCH', match: response}));
    }

    @boundMethod
    public reset(matchId: string): void {
        this.dispatch({type: 'SOCCER_MATCH_RESET', matchId});
        jQuery.ajax('/api/livematch/' + matchId + '/reset/', {
            method: 'POST',
            contentType: 'application/json'
        }).then((response) => this.dispatch({type: 'SOCCER_MATCH_SET_MATCH', match: response}));
    }

    protected dispatch(action: SoccerMatchAction): void {
        this.store.dispatch(action);
    }
}

let helperProvider = createSingleton(SoccerMatchActionsHelper);
export function getSoccerMatchActionsHelper(): SoccerMatchActionsHelper {
    return helperProvider.getInstance();
}
