import { createContext } from 'react';

// Context for selected sheet music ID to be shared between components
export const SheetMusicContext = createContext();
// Context for detected note to be shared between tuner and audio analyzer
export const TunerContext = createContext();
// Context for BPM to be shared between pages
export const BpmContext = createContext();
// Context for UI theme
export const ThemeContext = createContext();