import * as React from "react";
import {getSoccerMatchActionsHelper, SoccerMatch} from "./SoccerMatchActionsHelper";
import {Badge, Button, ButtonGroup, Card, Stack} from "react-bootstrap";
import {boundMethod} from "autobind-decorator";
import {Link, Navigate, useNavigate} from "react-router-dom";
import {connect} from "react-redux";
import {RootState} from "../AppStore";
import {SoccerMatchContainerComponent, SoccerMatchContainerProps} from "./SoccerMatchContainer";
import {SoccerMatchListUI} from "./SoccerMatchListUI";

export interface SoccerMatchListContainerProps {
    matches: SoccerMatch[];
}


export class SoccerMatchListContainerComponent extends React.Component<SoccerMatchListContainerProps, {}> {
    componentDidMount() {
        getSoccerMatchActionsHelper().fetchMatches();
    }

    @boundMethod
    private renderMatch(match: SoccerMatch): React.ReactNode {
        return <SoccerMatchListUI key={match.pk} match={match}/>
    }

    public render(): React.ReactNode {
        if (this.props.matches == null) {
            return <div>No soccer match available :(</div>;
        }
        return this.props.matches.map(this.renderMatch);
    }
}

export const SoccerMatchListContainer = connect(
    (store: RootState): SoccerMatchListContainerProps => ({
        matches: store?.soccerMatch?.matches,
    }),
)(SoccerMatchListContainerComponent);

