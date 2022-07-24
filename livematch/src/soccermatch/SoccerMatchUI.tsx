import * as React from "react";
import {getSoccerMatchActionsHelper, Player, SoccerMatch, Team} from "./SoccerMatchActionsHelper";
import {TeamUI} from "./TeamUI";
import {boundMethod} from "autobind-decorator";
import {Button, ButtonGroup, Modal} from "react-bootstrap";
import {Link} from "react-router-dom";
import classnames from 'classnames';

export interface SoccerMatchUIProps {
    match: SoccerMatch;
}

export interface SoccerMatchUIState {
    showModal: boolean;
    invertedOrder: boolean;
}

export class SoccerMatchUI extends React.Component<SoccerMatchUIProps, SoccerMatchUIState> {
    public state:SoccerMatchUIState = {showModal: false, invertedOrder: false};
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

    @boundMethod
    private handleSwitch(): void {
        this.setState({invertedOrder: !this.state.invertedOrder})
    }

    @boundMethod
    private handleLock(): void {
        getSoccerMatchActionsHelper().lock(this.props.match.pk);
    }

    @boundMethod
    private handleUnLock(): void {
        getSoccerMatchActionsHelper().unlock(this.props.match.pk);
    }

    private renderSwitchButton(): React.ReactNode {
        return <Button variant='primary' size='lg' onClick={this.handleSwitch}><i className='fa fa-arrow-right-arrow-left' /> Switch</Button>
    }

    private renderLockButton(): React.ReactNode {
        if (this.props.match.ended) {
            return <Button variant='outline-secondary' onClick={this.handleUnLock}><i className='fa fa-lock'/> Sblocca</Button>
        }

        return <Button variant='outline-secondary' onClick={this.handleLock}><i className='fa fa-lock'/> Fine</Button>;
    }

    private renderResetButton(): React.ReactNode {
        return (
            <Button variant='danger' size="lg" onClick={this.showModal} disabled={this.props.match.ended}>
                <i className='fa fa-exclamation-triangle'/> Reset
            </Button>
        );
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

        let classNames = classnames({
            'd-flex justify-content-evenly': true,
            'flex-row': !this.state.invertedOrder,
            'flex-row-reverse': this.state.invertedOrder,
        });

        return (
            <>
                <div className={classNames}>
                    <TeamUI key='team-a' team={this.props.match.team_a} score={this.props.match.score_a}
                            onScore={this.handleScore} disabled={this.props.match.ended} />
                    <TeamUI key='team-b' team={this.props.match.team_b} score={this.props.match.score_b}
                            onScore={this.handleScore}  disabled={this.props.match.ended} />

                </div>
                <div className='mt-4 d-flex justify-content-center'>
                    <ButtonGroup>
                        {this.renderGoBackButton()}
                        {this.renderSwitchButton()}
                        {this.renderLockButton()}
                        {this.renderResetButton()}
                    </ButtonGroup>
                </div>
                {this.renderResetModal()}
            </>
        );
    }
}