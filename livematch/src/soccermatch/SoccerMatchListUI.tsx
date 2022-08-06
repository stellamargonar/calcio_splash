import * as React from "react";
import {getSoccerMatchActionsHelper, SoccerMatch} from "./SoccerMatchActionsHelper";
import {boundMethod} from "autobind-decorator";
import {Badge, Button, ButtonGroup, Card} from "react-bootstrap";
import {Link} from "react-router-dom";
import { formatDate } from "../utils/Utils";

export interface SoccerMatchListUIProps {
    match: SoccerMatch;
}

export class SoccerMatchListUI extends React.Component<SoccerMatchListUIProps, {}> {
    @boundMethod
    private handleLock(): void {
        getSoccerMatchActionsHelper().lock(this.props.match.pk);
    }

    @boundMethod
    private handleUnLock(): void {
        getSoccerMatchActionsHelper().unlock(this.props.match.pk);
    }

    @boundMethod
    private renderGroup(): React.ReactNode {
        let variants = ['secondary', 'success', 'danger', 'warning', 'info', 'dark'],
            variant = variants[this.props.match.group.pk % variants.length];
        return <h5>Girone <Badge bg={variant}>{this.props.match.group.name}</Badge></h5>
    }

    private renderScore(): React.ReactNode {
        if (this.props.match.score_a == 0 && this.props.match.score_b == 0) {
            return "-"
        }
        return <h4>{this.props.match.score_a} - {this.props.match.score_b}</h4>
    }

    private renderLockButton(): React.ReactNode {
        if (this.props.match.team_a == null || this.props.match.team_b == null) {
            return null;
        }

        if (this.props.match.ended) {
            return <Button variant='outline-secondary' onClick={this.handleUnLock}>Sblocca <i className='fa fa-lock'/></Button>
        }

        return <Button variant='outline-secondary' onClick={this.handleLock}>Fine <i className='fa fa-lock'/></Button>;
    }

    private renderPlayButton(): React.ReactNode {
        if (this.props.match.team_a == null || this.props.match.team_b == null) {
            return null;
        }

        let disabledClass = this.props.match.ended ? 'disabled' : '';
        return (
            <Link
                to={`/livematch/play/${this.props.match.pk}`}
                className={`btn btn-primary btn-lg ${disabledClass}`}
            >
                Gioca{' '}
                <i className='fa fa-chevron-right'/>
            </Link>
        );
    }

    public render(): React.ReactNode {
        return (
            <Card key={`match-${this.props.match.pk}`} className='mb-4'>
                <Card.Header className='d-flex justify-content-between'>
                    <h5>{formatDate(this.props.match.date_time)}</h5>
                    {this.renderGroup()}
                </Card.Header>
                <Card.Body>
                    <Card.Title>{this.props.match.team_a?.name} vs {this.props.match.team_b?.name}</Card.Title>
                    <br />
                    {this.renderScore()}
                    <ButtonGroup style={{float: 'right'}}>
                            {this.renderLockButton()}
                            {this.renderPlayButton()}
                    </ButtonGroup>
                </Card.Body>
            </Card>
        );
    }
}
