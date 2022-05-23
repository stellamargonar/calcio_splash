import * as React from "react";
import {Player} from "./SoccerMatchActionsHelper";
import {boundMethod} from "autobind-decorator";
import {Badge, Button} from "react-bootstrap";


export interface PlayerUIProps {
    player: Player;
    onScore: (player: Player) => void;
}

export class PlayerUI extends React.PureComponent<PlayerUIProps> {

    @boundMethod
    private handleScore(): void {
        this.props.onScore(this.props.player);
    }

    private renderScore(): React.ReactNode {
        if (this.props.player.score === 0) {
            return null;

        }
        return <Badge bg="primary" pill>{this.props.player.score}</Badge>
    }


    public render(): React.ReactNode {
        return (
            <div onClick={this.handleScore} className="d-flex justify-content-between align-items-start">
                <h4>{this.props.player.name}</h4>
                    {this.renderScore()}
            </div>
        );
    }
}