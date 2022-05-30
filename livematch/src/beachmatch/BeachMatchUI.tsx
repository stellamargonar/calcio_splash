import * as React from "react";
import {getBeachMatchActionsHelper, Player, BeachMatch, Team} from "./BeachMatchActionsHelper";
import {boundMethod} from "autobind-decorator";
import {Button} from "react-bootstrap";

export interface BeachMatchUIProps {
    match: BeachMatch;
}

export class BeachMatchUI extends React.Component<BeachMatchUIProps, {}> {
    @boundMethod
    private handleScore(team: Team, set: number, remove?: boolean): void {
        getBeachMatchActionsHelper().score(this.props.match.pk, team.pk, set, remove);
    }
    @boundMethod
    private handleReset(): void {
        getBeachMatchActionsHelper().reset(this.props.match.pk);
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
                    {this.props.match.team_a.name} {this.props.match.team_a_set_1}
                    {this.props.match.team_b.name} {this.props.match.team_b_set_1}
                </div>
                <div className='mt-4 d-flex justify-content-center'>
                    {this.renderResetButton()}
                </div>
            </>
        );
    }
}