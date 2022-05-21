import * as React from "react";
import {getSoccerMatchActionsHelper, SoccerMatch} from "./SoccerMatchActionsHelper";
import {Button, Card, Stack} from "react-bootstrap";
import {boundMethod} from "autobind-decorator";
import {Link, Navigate, useNavigate} from "react-router-dom";
import {connect} from "react-redux";
import {RootState} from "../AppStore";
import {SoccerMatchContainerComponent, SoccerMatchContainerProps} from "./SoccerMatchContainer";

export interface SoccerMatchListContainerProps {
    matches: SoccerMatch[];
}


export class SoccerMatchListContainerComponent extends React.Component<SoccerMatchListContainerProps, {}> {
    componentDidMount() {
        getSoccerMatchActionsHelper().fetchMatches();
    }

    @boundMethod
    private renderMatch(match: SoccerMatch): React.ReactNode {
        return (
            <Card key={`match-${match.pk}`} className='mb-4'>
                <Card.Header>Sab 5 - 15:30</Card.Header>
                <Card.Body>
                    <Card.Title>{match.team_a.name} vs {match.team_b.name}</Card.Title>
                    <Card.Text>
                        5 - 6
                    <Link to={`/livematch/play/${match.pk}`} className='btn btn-primary btn-lg' style={{float: 'right'}}>Vai</Link>
                    </Card.Text>
                </Card.Body>
            </Card>
        );
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

