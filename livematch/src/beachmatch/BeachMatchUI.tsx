import * as React from "react";
import {getBeachMatchActionsHelper, BeachMatch, Team} from "./BeachMatchActionsHelper";
import {boundMethod} from "autobind-decorator";
import {Button, ButtonGroup} from "react-bootstrap";
import {BeachTeamUI} from "./BeachTeamUI";

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

    @boundMethod
    private handleAddSet(): void {
        getBeachMatchActionsHelper().addSet(this.props.match.pk)
    }

    private renderResetButton(): React.ReactNode {
        return <Button variant='secondary' onClick={this.handleReset}><i className='fa fa-exclamation-triangle' /> Reset</Button>
    }
    private renderAddSetButton(): React.ReactNode {
        if (!this.props.match.group.is_final) {
            return null;
        }
        return <Button variant='primary' onClick={this.handleAddSet}><i className='fa fa-plus' /> Add set</Button>
    }

    public render(): React.ReactNode {
        if (this.props.match == null) {
            return null;
        }

        return (
            <>
                <div className='d-flex flex-row justify-content-evenly'>
                    <BeachTeamUI
                        team={this.props.match.team_a}
                        score_set_1={this.props.match.team_a_set_1}
                        score_set_2={this.props.match.team_a_set_2}
                        score_set_3={this.props.match.team_a_set_3}
                        isFinal={this.props.match.group.is_final}
                        onScore={this.handleScore}
                    />
                    <BeachTeamUI
                        team={this.props.match.team_b}
                        score_set_1={this.props.match.team_b_set_1}
                        score_set_2={this.props.match.team_b_set_2}
                        score_set_3={this.props.match.team_b_set_3}
                        isFinal={this.props.match.group.is_final}
                        onScore={this.handleScore}
                    />
                </div>
                <div className='mt-4 d-flex justify-content-center'>
                    <ButtonGroup>
                        {this.renderResetButton()}
                        {this.renderAddSetButton()}
                    </ButtonGroup>
                </div>
            </>
        );
    }
}