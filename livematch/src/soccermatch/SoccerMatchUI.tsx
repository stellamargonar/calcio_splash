import * as React from "react";
import {getSoccerMatchActionsHelper, Player, SoccerMatch, Team} from "./SoccerMatchActionsHelper";
import {TeamUI} from "./TeamUI";
import {boundMethod} from "autobind-decorator";
import {Button} from "react-bootstrap";

export interface SoccerMatchUIProps {
    match: SoccerMatch;
}

export class SoccerMatchUI extends React.Component<SoccerMatchUIProps, {}> {
    @boundMethod
    private handleScore(team: Team, player: Player, remove?: boolean): void {
        getSoccerMatchActionsHelper().score(this.props.match.pk, team.pk, player?.pk, remove);
    }
    @boundMethod
    private handleReset(): void {
        getSoccerMatchActionsHelper().reset(this.props.match.pk);
    }

    private renderResetButton(): React.ReactNode {
        return <Button variant='secondary' onClick={this.handleReset}><i className='fa fa-exclamation-triangle' /> Reset</Button>
    }

    public render(): React.ReactNode {
        if (this.props.match == null) {
            return null;
        }

        return (
            <>
                <div className='d-flex flex-row justify-content-evenly'>
                    <TeamUI key='team-a' team={this.props.match.team_a} score={this.props.match.score_a}
                            onScore={this.handleScore}/>
                    <TeamUI key='team-b' team={this.props.match.team_b} score={this.props.match.score_b}
                            onScore={this.handleScore}/>

                </div>
                <div className='mt-4 d-flex justify-content-center'>
                    {this.renderResetButton()}
                </div>
            </>
        );
    }
}