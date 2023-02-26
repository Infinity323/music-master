import { Route, Routes } from 'react-router-dom'
import { createContext, useState } from 'react';
import './App.css';
import Home from './pages/Home';
import PracticeHistory from './pages/PracticeHistory';
import SheetMusic from './pages/SheetMusic';
import StartPracticeSession from './pages/StartPracticeSession';
import Tuner from './pages/Tuner';
import Recording from './pages/Recording';
import Performance from './pages/Performance';

export const baseUrl = "http://localhost:5000";

export const { style } = document.documentElement;

export const SheetMusicIdContext = createContext();

function App() {
  const [selectedMusic, setSelectedMusic] = useState(-1);
  return (
    <div className="App">
      <SheetMusicIdContext.Provider value={[selectedMusic, setSelectedMusic]}>
        <Routes>
          <Route path="/" element={<Home/>}/>
          <Route path="/tuner" element={<Tuner/>}/>
          <Route path="/history" element={<PracticeHistory/>}/>
          <Route path="/sheetmusic" element={<SheetMusic/>}/>
          <Route path="/startpracticesession" element={<StartPracticeSession/>}/>
          <Route path="/recording" element={<Recording/>}/>
          <Route path="/performance/:performanceId" element={<Performance/>}/>
        </Routes>
      </SheetMusicIdContext.Provider>
    </div>
  );
}

export default App;
