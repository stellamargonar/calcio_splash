import jQuery from 'jquery';
import {Store} from "@reduxjs/toolkit";
import {boundMethod} from 'autobind-decorator';
import {createSingleton} from "../utils/SingletonProvider";

export interface Player {
    pk: string;
    name: string;
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
  score: string;
}

export type SoccerMatchAction =
    | {type: 'SOCCER_MATCH_SET_MATCHES', matches: SoccerMatch[]}
    | {type: 'SOCCER_MATCH_SET_MATCH', match: SoccerMatch};



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

    protected dispatch(action: SoccerMatchAction): void {
        this.store.dispatch(action);
    }
    //
    // @boundMethod
    // public todo(id: string): void {
    //     this.dispatch({type: 'TODO2', id});
    // }
}

let helperProvider = createSingleton(SoccerMatchActionsHelper);
export function getSoccerMatchActionsHelper(): SoccerMatchActionsHelper {
    return helperProvider.getInstance();
}
