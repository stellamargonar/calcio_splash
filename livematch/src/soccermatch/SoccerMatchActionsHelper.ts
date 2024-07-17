import jQuery from 'jquery';
import {Store} from "@reduxjs/toolkit";
import {boundMethod} from 'autobind-decorator';
import {createSingleton} from "../utils/SingletonProvider";
import {initJQueryCSRF} from "../utils/Utils";

export interface Player {
    pk: string;
    full_name: string;
    nickname_or_full_name: string;
    score: number;
}

export interface Team {
    pk: string;
    name: string;
    players: Player[];
}

export interface Group {
    pk: number;
    name: string;
    tournament: string;
    is_final: boolean;
}

export interface SoccerMatch {
  pk: string;
  team_a: Team;
  team_b: Team;
  score_a: number;
  score_b: number;
  date_time: string;
  group: Group;
  ended: boolean;
}

export type SoccerMatchAction =
    | {type: 'SOCCER_MATCH_SET_MATCHES', matches: SoccerMatch[], showEnded: boolean}
    | {type: 'SOCCER_MATCH_SET_MATCH', match: SoccerMatch}
    | {type: 'SOCCER_MATCH_SCORE', matchId: string, teamId: string, playerId?: string, remove?: boolean}
    | {type: 'SOCCER_MATCH_RESET', matchId: string}
    | {type: 'SOCCER_MATCH_LOCK', matchId: string}
    | {type: 'SOCCER_MATCH_UNLOCK', matchId: string}
    | {type: 'SOCCER_MATCH_HIDE_ENDED', showEnded: boolean}
    | {type: 'SOCCER_MATCH_SET_LOADING', isLoading: boolean};

export class SoccerMatchActionsHelper {
    private store: Store;

    public setStore(store: Store): void {
        this.store = store;
    }

    @boundMethod
    private startLoading(): void {
        this.dispatch({type: 'SOCCER_MATCH_SET_LOADING', isLoading: true});
    }

    @boundMethod
    private stopLoading(): void {
        this.dispatch({type: 'SOCCER_MATCH_SET_LOADING', isLoading: false});
    }

    @boundMethod
    public fetchMatches(showEnded: boolean=false): void {
        this.startLoading();
        jQuery.ajax('/api/livematch/')
            .then((response ) => {
                this.stopLoading();
                this.dispatch({type: 'SOCCER_MATCH_SET_MATCHES', matches: response, showEnded})
            });
    }

    @boundMethod
    public fetchMatch(matchId: string): void {
        jQuery.ajax('/api/livematch/' + matchId)
            .then((response ) => {
                this.dispatch({type: 'SOCCER_MATCH_SET_MATCH', match: response})
            });
    }

    @boundMethod
    public score(matchId: string, teamId: string, playerId?: string, remove?: boolean): void {
        this.dispatch({type: 'SOCCER_MATCH_SCORE', matchId, teamId, playerId, remove});
        initJQueryCSRF();
        jQuery.ajax('/api/livematch/' + matchId + '/score/', {
            method: 'POST',
            data: JSON.stringify({teamId, playerId, remove}),
            contentType: 'application/json'
        }).then((response) => this.dispatch({type: 'SOCCER_MATCH_SET_MATCH', match: response}));
    }

    @boundMethod
    public reset(matchId: string): void {
        this.dispatch({type: 'SOCCER_MATCH_RESET', matchId});
        initJQueryCSRF();
        jQuery.ajax('/api/livematch/' + matchId + '/reset/', {
            method: 'POST',
            contentType: 'application/json'
        }).then((response) => this.dispatch({type: 'SOCCER_MATCH_SET_MATCH', match: response}));
    }

    @boundMethod
    public lock(matchId: string): void {
        this.dispatch({type: 'SOCCER_MATCH_LOCK', matchId});
        initJQueryCSRF();
        jQuery.ajax('/api/livematch/' + matchId + '/lock/', {
            method: 'POST',
            contentType: 'application/json'
        }).then((response) => this.dispatch({type: 'SOCCER_MATCH_SET_MATCH', match: response}));
    }

    @boundMethod
    public unlock(matchId: string): void {
        this.dispatch({type: 'SOCCER_MATCH_UNLOCK', matchId});
        initJQueryCSRF();
        jQuery.ajax('/api/livematch/' + matchId + '/unlock/', {
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
