import * as React from "react";
import {Player, SoccerMatch, Team} from "./SoccerMatchActionsHelper";
import {Container} from "react-bootstrap";
import {boundMethod} from "autobind-decorator";

export interface SoccerMatchUIProps {
    match: SoccerMatch;
}

export class SoccerMatchUI extends React.Component<SoccerMatchUIProps, {}> {

    @boundMethod
    private renderPlayer(player: Player): React.ReactNode{
        return (
          <div>
              {player.name} (3)
          </div>
        );
    }

    private renderTeam(team: Team): React.ReactNode {
        return (
            <div className='flex-grow-1'>
                {team.name }
                {team.players.map(this.renderPlayer)}
            </div>
        );
    }

    private renderTeamA(): React.ReactNode {
        return this.renderTeam(this.props.match.team_a)
    }

    private renderTeamB(): React.ReactNode {
        return this.renderTeam(this.props.match.team_b)
    }

    private renderScore(): React.ReactNode {
        return <>{this.props.match.score}</>;
    }

    public render(): React.ReactNode {
        if (this.props.match == null) {
            return null;
        }

        return (
            <Container className='d-flex flex-row justify-content-around' >
                <div>
                    {this.renderTeamA()}
                </div>
                <div>{this.renderScore()}</div>
                <div>
                    {this.renderTeamB()}
                </div>
            </Container>
        );
    }
}