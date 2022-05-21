import { configureStore } from '@reduxjs/toolkit'
import {SoccerMatchReducer} from "./soccermatch/SoccerMatchReducer";


export const store = configureStore({
  reducer: {
    soccerMatch: SoccerMatchReducer.reducer,
  },
});

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
