import * as React from "react";
import {useParams} from "react-router-dom";
import {connect} from "react-redux";
import {RootState} from "../AppStore";
import {BeachMatch, getBeachMatchActionsHelper} from "./BeachMatchActionsHelper";
import {BeachMatchUI} from "./BeachMatchUI";


export interface BeachMatchContainerProps {
    match: BeachMatch;
}


export const BeachMatchContainerComponent = (props: BeachMatchContainerProps) => {
    let {matchId} = useParams();
    if (props.match == null || props.match.pk != matchId) {
        getBeachMatchActionsHelper().fetchMatch(matchId);
    }
    return <BeachMatchUI match={props.match} />;
}


export const BeachMatchContainer = connect(
    (store: RootState): BeachMatchContainerProps => ({
        match: store?.beachMatch?.match,
    }),
)(BeachMatchContainerComponent);

