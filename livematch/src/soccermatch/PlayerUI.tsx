import * as React from "react";
import {Player} from "./SoccerMatchActionsHelper";
import {boundMethod} from "autobind-decorator";
import {Badge, Button, ListGroupItem} from "react-bootstrap";
import {EllipsableContent} from "../EllipsableContent";


export interface PlayerUIProps {
    player: Player;
    onScore: (player: Player, remove?: boolean) => void;
    disabled: boolean;
}

export class PlayerUI extends React.PureComponent<PlayerUIProps> {

    @boundMethod
    private handleScoreUp(): void {
        this.props.onScore(this.props.player);
    }
    @boundMethod
    private handleScoreDown(): void {
        this.props.onScore(this.props.player, true);
    }

    private renderButtonScoreUp(): React.ReactNode {
        return <Button className='btn-success' onClick={this.handleScoreUp} disabled={this.props.disabled}>+</Button>;
    }

    private renderButtonScoreDown(): React.ReactNode {
        return <Button className='btn-danger' onClick={this.handleScoreDown} disabled={this.props.disabled}>-</Button>;
    }

    private renderScore(): React.ReactNode {
        if (this.props.player.score === 0) {
            return null;

        }
        return <Badge bg="primary" pill>{this.props.player.score}</Badge>
    }

    private renderLabel(): React.ReactNode {
        return <div className='flex-grow-1 d-flex justify-content-center align-items-center p-1'>
            <div className="flex-grow-1 d-flex flex-column justify-content-center">
                <span><EllipsableContent value={this.props.player.full_name} /></span>
                {this.props.player.nickname != null && (<em><EllipsableContent value={`(${this.props.player.nickname})`} /></em>)}
            </div>
            <div>
                {this.renderScore()}
            </div>
        </div>
    }

    public render(): React.ReactNode {
        return (
            <ListGroupItem className='d-flex flex-row player-container'>
                {this.renderButtonScoreDown()}
                {this.renderLabel()}
                {this.renderButtonScoreUp()}
            </ListGroupItem>

        );
    }
}
