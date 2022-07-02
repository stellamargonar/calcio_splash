import * as React from "react";
import {getSoccerMatchActionsHelper, SoccerMatch} from "./SoccerMatchActionsHelper";
import {useParams} from "react-router-dom";
import {connect} from "react-redux";
import {RootState} from "../AppStore";
import {SoccerMatchUI} from "./SoccerMatchUI";
import {Loader} from "../Loader";


export interface SoccerMatchContainerProps {
    match: SoccerMatch;
    isLoading: boolean;
}


export const SoccerMatchContainerComponent = (props: SoccerMatchContainerProps) => {
    let {matchId} = useParams();
    if (props.match == null || props.match.pk != matchId) {
        getSoccerMatchActionsHelper().fetchMatch(matchId);
    }
    if (props.isLoading) {
        return <Loader />;
    }
    return <SoccerMatchUI match={props.match} />;
}


export const SoccerMatchContainer = connect(
    (store: RootState): SoccerMatchContainerProps => ({
        match: store?.soccerMatch?.match,
        isLoading: store?.soccerMatch?.isLoading,
    }),
)(SoccerMatchContainerComponent);

