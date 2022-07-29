import * as React from "react";
import {getBeachMatchActionsHelper, BeachMatch, Team} from "./BeachMatchActionsHelper";
import {boundMethod} from "autobind-decorator";
import {Button, ButtonGroup, Modal} from "react-bootstrap";
import {BeachTeamUI} from "./BeachTeamUI";
import {Link} from "react-router-dom";
import classnames from "classnames";

export interface BeachMatchUIProps {
    match: BeachMatch;
}

export interface BeachMatchUIState {
    showModal: boolean;
    invertedOrder: boolean;
}

export class BeachMatchUI extends React.Component<BeachMatchUIProps, BeachMatchUIState> {
    public state: BeachMatchUIState = {showModal: false, invertedOrder: false};

    @boundMethod
    private handleScore(team: Team, set: number, remove?: boolean): void {
        getBeachMatchActionsHelper().score(this.props.match.pk, team.pk, set, remove);
    }

    @boundMethod
    private handleReset(): void {
        getBeachMatchActionsHelper().reset(this.props.match.pk);
        this.hideModal();
    }

    @boundMethod
    private handleAddSet(): void {
        getBeachMatchActionsHelper().addSet(this.props.match.pk)
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
    private handleLock(): void {
        getBeachMatchActionsHelper().lock(this.props.match.pk);
    }

    @boundMethod
    private handleUnLock(): void {
        getBeachMatchActionsHelper().unlock(this.props.match.pk);
    }

    @boundMethod
    private handleSwitch(): void {
        this.setState({invertedOrder: !this.state.invertedOrder})
    }

    private renderSwitchButton(): React.ReactNode {
        return <Button variant='primary' size='lg' onClick={this.handleSwitch}><i className='fa fa-arrow-right-arrow-left' /> Switch</Button>
    }

    private renderResetButton(): React.ReactNode {
        return (
            <Button variant='danger' size='lg' onClick={this.showModal}  disabled={this.props.match.ended}>
                <i className='fa fa-exclamation-triangle'/>{' '}Reset
            </Button>
        );
    }
    private renderLockButton(): React.ReactNode {
        if (this.props.match.ended) {
            return <Button variant='outline-secondary' onClick={this.handleUnLock}><i className='fa fa-lock'/> Sblocca</Button>
        }

        return <Button variant='outline-secondary' onClick={this.handleLock}><i className='fa fa-lock'/> Fine</Button>;
    }

    private renderAddSetButton(): React.ReactNode {
        if (!this.props.match.group.is_final) {
            return null;
        }
        return (
            <Button size='lg' variant='success' onClick={this.handleAddSet} disabled={this.props.match.ended}>
                <i className='fa fa-plus'/>{' '}
                Add set
            </Button>
        );
    }

    private renderGoBackButton(): React.ReactNode {
        return (
            <Link to={'/beachmatch/'} className='btn btn-primary btn-lg'>
                <i className='fa fa-chevron-left'/>{' '}
                Lista Partite
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
                    <p>Attenzione, cancellerai tutti i punti di tutti i set della partita. Non si può tornare
                        indietro.</p>
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
                    <BeachTeamUI
                        team={this.props.match.team_a}
                        score_set_1={this.props.match.team_a_set_1}
                        score_set_2={this.props.match.team_a_set_2}
                        score_set_3={this.props.match.team_a_set_3}
                        isFinal={this.props.match.group.is_final}
                        onScore={this.handleScore}
                        disabled={this.props.match.ended}
                    />
                    <BeachTeamUI
                        team={this.props.match.team_b}
                        score_set_1={this.props.match.team_b_set_1}
                        score_set_2={this.props.match.team_b_set_2}
                        score_set_3={this.props.match.team_b_set_3}
                        isFinal={this.props.match.group.is_final}
                        onScore={this.handleScore}
                        disabled={this.props.match.ended}
                    />
                </div>
                <div className='mt-4 d-flex justify-content-center'>
                    <ButtonGroup>
                        {this.renderGoBackButton()}
                        {this.renderAddSetButton()}
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