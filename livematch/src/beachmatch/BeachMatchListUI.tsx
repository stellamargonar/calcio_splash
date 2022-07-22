import * as React from "react";
import {boundMethod} from "autobind-decorator";
import {Badge, ButtonGroup, Card} from "react-bootstrap";
import {Link} from "react-router-dom";
import {BeachMatch} from "./BeachMatchActionsHelper";

export interface BeachMatchListUIProps {
    match: BeachMatch;
}

export class BeachMatchListUI extends React.Component<BeachMatchListUIProps, {}> {
    @boundMethod
    private renderGroup(): React.ReactNode {
        let variants = ['secondary', 'success', 'danger', 'warning', 'info', 'dark'],
            variant = variants[this.props.match.group.pk % variants.length];
        return <h5>Girone <Badge bg={variant}>{this.props.match.group.name}</Badge></h5>
    }

    private renderScore(): React.ReactNode {
        if (this.props.match.team_a_set_1 == 0 && this.props.match.team_b_set_1 == 0) {
            return "-"
        }
        return <span>{this.props.match.team_a_set_1} - {this.props.match.team_b_set_1}</span>
    }


    private renderPlayButton(): React.ReactNode {
        return (
            <Link
                to={`/beachmatch/play/${this.props.match.pk}`}
                className='btn btn-primary btn-lg'
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
                    <h5>{this.props.match.date_time}</h5>
                    {this.renderGroup()}
                </Card.Header>
                <Card.Body>
                    <Card.Title>{this.props.match.team_a.name} vs {this.props.match.team_b.name}</Card.Title>
                    <Card.Text>
                        {this.renderScore()}
                    </Card.Text>
                    <ButtonGroup style={{float: 'right'}}>
                        {this.renderPlayButton()}
                    </ButtonGroup>
                </Card.Body>
            </Card>
        );
    }
}