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
                <PlayerUI key={`player-${player.pk}`} player={player} onScore={this.handleGoalPlayer}/>
        );
    }

    private renderLabel(): React.ReactNode {
        return <div className='flex-grow-1'><h1>{this.props.team.name} {this.props.score}</h1></div>;
    }

    public render(): React.ReactNode {
        return (
            <Card className='team-card'>
                <Card.Body>
                    <Card.Title className='d-grid gap-2 d-flex flex-row team-container'>
                        <Button size='lg' variant='danger' onClick={this.handleGoalTeamDown}>-</Button>
                        {this.renderLabel()}
                        <Button size='lg' variant='success' onClick={this.handleGoalTeamUp}>+</Button>
                    </Card.Title>
                    <ListGroup variant="flush">
                        {this.props.team.players.map(this.renderPlayer)}
                    </ListGroup>
                </Card.Body>
            </Card>
        );
    }
}