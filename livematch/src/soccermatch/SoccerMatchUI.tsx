import * as React from "react";
import {getSoccerMatchActionsHelper, Player, SoccerMatch, Team} from "./SoccerMatchActionsHelper";
import {TeamUI} from "./TeamUI";
import {boundMethod} from "autobind-decorator";
import {Button, ButtonGroup, Modal} from "react-bootstrap";
import {Link} from "react-router-dom";

export interface SoccerMatchUIProps {
    match: SoccerMatch;
}

export interface SoccerMatchUIState {
    showModal: boolean;
}

export class SoccerMatchUI extends React.Component<SoccerMatchUIProps, SoccerMatchUIState> {
    public state:SoccerMatchUIState = {showModal: false};
    @boundMethod
    private handleScore(team: Team, player: Player, remove?: boolean): void {
        getSoccerMatchActionsHelper().score(this.props.match.pk, team.pk, player?.pk, remove);
    }
    @boundMethod
    private handleReset(): void {
        getSoccerMatchActionsHelper().reset(this.props.match.pk);
        this.hideModal();
    }

    @boundMethod
    private hideModal(): void {
        this.setState({showModal: false});
    }

    @boundMethod
    private showModal(): void {
        this.setState({showModal: true});
    }

    private renderResetButton(): React.ReactNode {
        return <Button variant='secondary' size="lg" onClick={this.showModal}><i className='fa fa-exclamation-triangle' /> Reset</Button>
    }

    private renderGoBackButton(): React.ReactNode {
        return (
            <Link to={'/livematch/'} className='btn btn-primary btn-lg'>
                <i className='fa fa-chevron-left'/>
                Lista Partite{' '}
            </Link>
        );
    }

    private renderResetModal(): React.ReactNode {
        return (
            <Modal show={this.state.showModal} onHide={this.hideModal} centered>
                <Modal.Header closeButton>
                    <Modal.Title>Vuoi resettare questa partita?</Modal.Title>
                </Modal.Header>

                <Modal.Body>
                    <p>Attenzione, cancellerai tutti i goal della partita. Non si può tornare indietro.</p>
                </Modal.Body>

                <Modal.Footer>
                    <Button variant="secondary" onClick={this.hideModal}>Chiudi</Button>
                    <Button variant="danger" onClick={this.handleReset}>Cancella tutto</Button>
                </Modal.Footer>
            </Modal>
        );
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
                    <ButtonGroup>
                        {this.renderGoBackButton()}
                        {this.renderResetButton()}
                    </ButtonGroup>
                </div>
                {this.renderResetModal()}
            </>
        );
    }
}