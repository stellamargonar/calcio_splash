import * as React from "react";
import {Player, Team} from "./SoccerMatchActionsHelper";
import {boundMethod} from "autobind-decorator";
import {PlayerUI} from "./PlayerUI";
import {Button, Card, ListGroup} from "react-bootstrap";


export interface TeamUIProps {
    team: Team;
    score: number;
    onScore: (team: Team, player?: Player, remove?: boolean) => void;
}

export class TeamUI extends React.PureComponent<TeamUIProps> {
    @boundMethod
    private handleGoalTeamUp(): void {
        this.props.onScore(this.props.team);
    }
    @boundMethod
    private handleGoalTeamDown(): void {
        this.props.onScore(this.props.team, null, true);
    }

    @boundMethod
    private handleGoalPlayer(player: Player, remove?: boolean): void {
        this.props.onScore(this.props.team, player, remove);
    }

    @boundMethod
    private renderPlayer(player: Player): React.ReactNode {
        return (
            <ListGroup.Item key={`player-${player.pk}`} >
                <PlayerUI player={player} onScore={this.handleGoalPlayer}/>
            </ListGroup.Item>
        );
    }

    public render(): React.ReactNode {
        return (
            <Card className='team-card'>
                <Card.Body>
                    <Card.Title className='d-grid gap-2'>
                        <Button size='lg' variant='light' onClick={this.handleGoalTeamUp}>
                            <h1>{this.props.team.name}</h1>
                            <span className='pull-right'>{this.props.score}</span>
                        </Button>
                    </Card.Title>
                    <ListGroup variant="flush">
                        {this.props.team.players.map(this.renderPlayer)}
                    </ListGroup>
                </Card.Body>
            </Card>
        );
    }
}