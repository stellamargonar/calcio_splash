import * as React from "react";
import {Button, ButtonGroup} from "react-bootstrap";
import {boundMethod} from "autobind-decorator";
import {connect} from "react-redux";
import {RootState} from "../AppStore";
import {BeachMatch, getBeachMatchActionsHelper} from "./BeachMatchActionsHelper";
import {BeachMatchListUI} from "./BeachMatchListUI";

export interface BeachMatchListContainerProps {
    matches: BeachMatch[];
}

export interface BeachMatchListContainerState {
    showEnded: boolean;
}

export class BeachMatchListContainerComponent extends React.Component<BeachMatchListContainerProps, BeachMatchListContainerState> {
    public state: BeachMatchListContainerState = {showEnded: true};

    componentDidMount() {
        getBeachMatchActionsHelper().fetchMatches();
    }

    @boundMethod
    private handleToggleEnded(): void {
        getBeachMatchActionsHelper().fetchMatches(!this.state.showEnded);
        this.setState({showEnded: !this.state.showEnded});
    }

    @boundMethod
    private renderMatch(match: BeachMatch): React.ReactNode {
        return <BeachMatchListUI key={match.pk} match={match}/>
    }

    private renderHideEndedButton(): React.ReactNode {
        if (this.state.showEnded) {
            return (
                <Button variant='outline-light' onClick={this.handleToggleEnded}>
                    Nascondi finite <i className='fa fa-eye-slash'/>
                </Button>
            );
        }
        return (
            <Button variant='outline-light' onClick={this.handleToggleEnded}>
                Mostra tutte <i className='fa fa-eye'/>
            </Button>
        );
    }

    private renderHeader(): React.ReactNode {
        return (
            <div className='topbar d-flex mb-4 bg-primary p-3 justify-content-between'>
                <h1 style={{color: 'white'}}>Partite torneo 2022</h1>
                <ButtonGroup>
                    {this.renderHideEndedButton()}
                </ButtonGroup>
            </div>
        );
    }

    public render(): React.ReactNode {
        if (this.props.matches == null) {
            return <div>No beach match available :(</div>;
        }
        return (
            <div>
                {this.renderHeader()}
                {this.props.matches.map(this.renderMatch)}
            </div>
        );
    }
}

export const BeachMatchListContainer = connect(
    (store: RootState): BeachMatchListContainerProps => ({
        matches: store?.beachMatch?.matches,
    }),
)(BeachMatchListContainerComponent);

