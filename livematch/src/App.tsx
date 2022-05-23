import * as React from "react";
import {RootState, store} from "./AppStore";
import {SoccerMatchListContainer} from "./soccermatch/SoccerMatchListContainer";
import {getSoccerMatchActionsHelper} from "./soccermatch/SoccerMatchActionsHelper";
import {Container, ThemeProvider} from "react-bootstrap";
import {BrowserRouter, Route, Routes, useParams} from "react-router-dom";
import {SoccerMatchContainer} from "./soccermatch/SoccerMatchContainer";
import {Provider} from "react-redux";


export class LiveMatchApp extends React.Component<{}, RootState> {
    constructor(props: any) {
        super(props);
        store.subscribe(() => this.setState(store.getState()));
        getSoccerMatchActionsHelper().setStore(store);
        this.state = store.getState();
    }

    private renderSingleMatch(): React.ReactNode {
        return <SoccerMatchContainer />;
    }

    private renderMatchList(): React.ReactNode {
        return <SoccerMatchListContainer />;
    }

    public render(): React.ReactNode {
        return (
            <Provider store={store}>
                <ThemeProvider>
                    <div className='m-2'>
                    <BrowserRouter>
                        <Routes>
                            <Route path='/livematch/play/:matchId' element={this.renderSingleMatch()}/>
                            <Route path='/livematch/' element={this.renderMatchList()}/>
                        </Routes>
                    </BrowserRouter>
                    </div>
                </ThemeProvider>
            </Provider>
        );
    }
}

