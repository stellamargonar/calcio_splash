import * as React from "react";
import {getSoccerMatchActionsHelper, SoccerMatch} from "./SoccerMatchActionsHelper";
import {Badge, Button, ButtonGroup, Card, Stack} from "react-bootstrap";
import {boundMethod} from "autobind-decorator";
import {Link, Navigate, useNavigate} from "react-router-dom";
import {connect} from "react-redux";
import {RootState} from "../AppStore";
import {SoccerMatchContainerComponent, SoccerMatchContainerProps} from "./SoccerMatchContainer";
import {SoccerMatchListUI} from "./SoccerMatchListUI";

export interface SoccerMatchListContainerProps {
    matches: SoccerMatch[];
}

export interface SoccerMatchListContainerState {
    showEnded: boolean;
}

export class SoccerMatchListContainerComponent extends React.Component<SoccerMatchListContainerProps, SoccerMatchListContainerState> {
    public state: SoccerMatchListContainerState = {showEnded: true};

    componentDidMount() {
        getSoccerMatchActionsHelper().fetchMatches();
    }

    @boundMethod
    private handleToggleEnded(): void {
        getSoccerMatchActionsHelper().fetchMatches(!this.state.showEnded);
        this.setState({showEnded: !this.state.showEnded});
    }

    @boundMethod
    private handleGenerateNewMatches(): void {
        getSoccerMatchActionsHelper().generateMatches(this.state.showEnded);
    }

    @boundMethod
    private renderMatch(match: SoccerMatch): React.ReactNode {
        return <SoccerMatchListUI key={match.pk} match={match}/>
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
                    <Button variant='outline-light' onClick={this.handleGenerateNewMatches}>Genera prossime partite  <i className='fa fa-gear' /></Button>
                </ButtonGroup>
            </div>
        );
    }

    public render(): React.ReactNode {
        if (this.props.matches == null) {
            return <div>No soccer match available :(</div>;
        }
        return (
            <div>
                {this.renderHeader()}
                {this.props.matches.map(this.renderMatch)}
            </div>
        );
    }
}

export const SoccerMatchListContainer = connect(
    (store: RootState): SoccerMatchListContainerProps => ({
        matches: store?.soccerMatch?.matches,
    }),
)(SoccerMatchListContainerComponent);

