import { createContext } from 'react';

// Context for selected sheet music ID to be shared between components
export const SheetMusicIdContext = createContext();
// Context for detected note to be shared between tuner and audio analyzer
export const TunerContext = createContext();