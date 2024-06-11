import * as React from "react";
import {getSoccerMatchActionsHelper, SoccerMatch} from "./SoccerMatchActionsHelper";
import {Button, ButtonGroup} from "react-bootstrap";
import {boundMethod} from "autobind-decorator";
import {connect} from "react-redux";
import {RootState} from "../AppStore";
import {SoccerMatchListUI} from "./SoccerMatchListUI";
import {Loader} from "../Loader";

export interface SoccerMatchListContainerProps {
    matches: SoccerMatch[];
    isLoading: boolean;
}

export interface SoccerMatchListContainerState {
    showEnded: boolean;
}

export class SoccerMatchListContainerComponent extends React.Component<SoccerMatchListContainerProps, SoccerMatchListContainerState> {
    public state: SoccerMatchListContainerState = {showEnded: false};

    componentDidMount() {
        getSoccerMatchActionsHelper().fetchMatches(this.state.showEnded);
    }

    @boundMethod
    private handleToggleEnded(): void {
        getSoccerMatchActionsHelper().fetchMatches(!this.state.showEnded);
        this.setState({showEnded: !this.state.showEnded});
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
                <h1 style={{color: 'white'}}>Partite torneo 2024</h1>
                <ButtonGroup>
                    {this.renderHideEndedButton()}
                </ButtonGroup>
            </div>
        );
    }

    private renderLoader(): React.ReactNode {
        if (!this.props.isLoading) {
            return null;
        }
        return <Loader />;
    }

    public render(): React.ReactNode {
        if (this.props.matches == null) {
            return <div>No soccer match available :(</div>;
        }
        return (
            <div>
                {this.renderHeader()}
                {this.renderLoader()}
                {this.props.matches.map(this.renderMatch)}
            </div>
        );
    }
}

export const SoccerMatchListContainer = connect(
    (store: RootState): SoccerMatchListContainerProps => ({
        matches: store?.soccerMatch?.matches,
        isLoading: store?.soccerMatch?.isLoading,
    }),
)(SoccerMatchListContainerComponent);

