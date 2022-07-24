import jQuery from 'jquery';
import {Store} from "@reduxjs/toolkit";
import {boundMethod} from 'autobind-decorator';
import {createSingleton} from "../utils/SingletonProvider";
import {initJQueryCSRF} from "../utils/Utils";

export interface Player {
    pk: string;
    name: string;
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

export interface BeachMatch {
  pk: string;
  team_a: Team;
  team_b: Team;
  date_time: string;
  group: Group;
  team_a_set_1: number;
  team_b_set_1: number;
  team_a_set_2: number;
  team_b_set_2: number;
  team_a_set_3: number;
  team_b_set_3: number;

}

export type BeachMatchAction =
    | {type: 'BEACH_MATCH_SET_MATCHES', matches: BeachMatch[], showEnded: boolean}
    | {type: 'BEACH_MATCH_SET_MATCH', match: BeachMatch}
    | {type: 'BEACH_MATCH_SCORE', matchId: string, teamId: string, set: number, remove?: boolean}
    | {type: 'BEACH_MATCH_RESET', matchId: string}
    | {type: 'BEACH_MATCH_ADD_SET', matchId: string}
    | {type: 'BEACH_MATCH_LOCK', matchId: string}
    | {type: 'BEACH_MATCH_UNLOCK', matchId: string}
    | {type: 'BEACH_MATCH_HIDE_ENDED', showEnded: boolean};


export class BeachMatchActionsHelper {
    private store: Store;

    public setStore(store: Store): void {
        this.store = store;
    }

    @boundMethod
    public fetchMatches(showEnded: boolean=false): void {
        jQuery.ajax('/api/beachmatch/')
            .then((response ) => this.dispatch({type: 'BEACH_MATCH_SET_MATCHES', matches: response, showEnded}));
    }

    @boundMethod
    public fetchMatch(matchId: string): void {
        jQuery.ajax('/api/beachmatch/' + matchId)
            .then((response ) => this.dispatch({type: 'BEACH_MATCH_SET_MATCH', match: response}));
    }

    @boundMethod
    public score(matchId: string, teamId: string, set: number = 1, remove?: boolean): void {
        this.dispatch({type: 'BEACH_MATCH_SCORE', matchId, teamId, set, remove});
        initJQueryCSRF();
        jQuery.ajax('/api/beachmatch/' + matchId + '/score/', {
            method: 'POST',
            data: JSON.stringify({teamId, set, remove}),
            contentType: 'application/json'
        }).then((response) => this.dispatch({type: 'BEACH_MATCH_SET_MATCH', match: response}));
    }

    @boundMethod
    public reset(matchId: string): void {
        this.dispatch({type: 'BEACH_MATCH_RESET', matchId});
        initJQueryCSRF();
        jQuery.ajax('/api/beachmatch/' + matchId + '/reset/', {
            method: 'POST',
            contentType: 'application/json'
        }).then((response) => this.dispatch({type: 'BEACH_MATCH_SET_MATCH', match: response}));
    }

    @boundMethod
    public addSet(matchId: string): void {
        this.dispatch({type: 'BEACH_MATCH_ADD_SET', matchId});
        initJQueryCSRF();
        jQuery.ajax('/api/beachmatch/' + matchId + '/add-set/', {
            method: 'POST',
            contentType: 'application/json'
        }).then((response) => this.dispatch({type: 'BEACH_MATCH_SET_MATCH', match: response}));
    }

    protected dispatch(action: BeachMatchAction): void {
        this.store.dispatch(action);
    }
}

let helperProvider = createSingleton(BeachMatchActionsHelper);
export function getBeachMatchActionsHelper(): BeachMatchActionsHelper {
    return helperProvider.getInstance();
}
