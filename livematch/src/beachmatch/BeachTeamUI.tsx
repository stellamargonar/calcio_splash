import * as React from "react";
import {boundMethod} from "autobind-decorator";
import {Button, Card, ListGroup, ListGroupItem} from "react-bootstrap";
import {Team} from "./BeachMatchActionsHelper";


export interface BeachTeamUIProps {
    team: Team;
    score_set_1: number;
    score_set_2?: number;
    score_set_3?: number;
    isFinal: boolean;
    onScore: (team: Team, currentSet: number, remove?: boolean) => void;
}


export class BeachTeamUI extends React.PureComponent<BeachTeamUIProps> {
    @boundMethod
    private handleScoreUp(currentSet: number): void {
        this.props.onScore(this.props.team, currentSet);
    }
    @boundMethod
    private handleScoreDown(currentSet: number): void {
        this.props.onScore(this.props.team, currentSet, true);
    }

    private renderLabel(): React.ReactNode {
        return <div className='flex-grow-1'><h1>{this.props.team.name}</h1></div>;
    }

    private renderSet(set: number): React.ReactNode {
        if (set > 1 && !this.props.isFinal) {
            return null;
        }
        let score = (set === 1) ? this.props.score_set_1 : (set === 2) ? this.props.score_set_2 : this.props.score_set_3;
        if (score == null) {
            return null;
        }
        return (
            <ListGroupItem className='d-flex flex-row beach-team-set'>
                <Button size='lg' variant='danger' onClick={() => this.handleScoreDown(set)}>-</Button>
                <h2>{score}</h2>
                <Button size='lg' variant='success' onClick={() => this.handleScoreUp(set)}>+</Button>
            </ListGroupItem>
        );
    }

    public render(): React.ReactNode {
        return (
            <Card className='team-card'>
                <Card.Body>
                    <Card.Title className='d-grid gap-2 d-flex flex-row team-container'>
                        {this.renderLabel()}
                    </Card.Title>
                    <ListGroup variant='flush'>
                        {this.renderSet(1)}
                        {this.renderSet(2)}
                        {this.renderSet(3)}
                    </ListGroup>
                </Card.Body>
            </Card>
        );
    }
}