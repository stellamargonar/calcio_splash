import { configureStore } from '@reduxjs/toolkit'
import {SoccerMatchReducer} from "./soccermatch/SoccerMatchReducer";
import {BeachMatchReducer} from "./beachmatch/BeachMatchReducer";


export const store = configureStore({
  reducer: {
    soccerMatch: SoccerMatchReducer.reducer,
    beachMatch: BeachMatchReducer.reducer,
  },
});

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
