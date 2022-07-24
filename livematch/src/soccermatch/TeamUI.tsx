import * as React from "react";
import {Player, Team} from "./SoccerMatchActionsHelper";
import {boundMethod} from "autobind-decorator";
import {PlayerUI} from "./PlayerUI";
import {Button, Card, ListGroup} from "react-bootstrap";
import {EllipsableContent} from "../EllipsableContent";


export interface TeamUIProps {
    team: Team;
    score: number;
    onScore: (team: Team, player?: Player, remove?: boolean) => void;
    disabled: boolean;
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
            <PlayerUI key={`player-${player.pk}`} player={player} onScore={this.handleGoalPlayer} disabled={this.props.disabled}/>
        );
    }

    private renderLabel(): React.ReactNode {
        return <div className='flex-grow-1'><h1><EllipsableContent value={this.props.team.name} /><br />{this.props.score}</h1></div>;
    }

    public render(): React.ReactNode {
        return (
            <Card className='team-card'>
                <Card.Body>
                    <Card.Title className='d-grid gap-2 d-flex flex-row team-container'>
                        <Button size='lg' variant='danger' onClick={this.handleGoalTeamDown} disabled={this.props.disabled}>-</Button>
                        {this.renderLabel()}
                        <Button size='lg' variant='success' onClick={this.handleGoalTeamUp}  disabled={this.props.disabled}>+</Button>
                    </Card.Title>
                    <ListGroup variant="flush">
                        {this.props.team.players.map(this.renderPlayer)}
                    </ListGroup>
                </Card.Body>
            </Card>
        );
    }
}