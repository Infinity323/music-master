import { Route, Routes } from 'react-router-dom'
import { useState } from 'react';
import './App.css';
import Home from './pages/Home';
import PracticeHistory from './pages/PracticeHistory';
import SheetMusic from './pages/SheetMusic';
import StartPracticeSession from './pages/StartPracticeSession';
import TunerMetronome from './pages/TunerMetronome';
import Recording from './pages/Recording';
import Performance from './pages/Performance';
import { BpmContext, SheetMusicIdContext, TunerContext } from './utils/Contexts';

export const baseUrl = "http://127.0.0.1:5000";

export const { style } = document.documentElement;

function App() {
  const [selectedMusic, setSelectedMusic] = useState(-1);
  const [currentNote, setCurrentNote] = useState(-1);
  const [bpm, setBpm] = useState(100);

  return (
    <div className="App">
      <SheetMusicIdContext.Provider value={[selectedMusic, setSelectedMusic]}>
        <TunerContext.Provider value={[currentNote, setCurrentNote]}>
          <BpmContext.Provider value={[bpm, setBpm]}>
            <Routes>
              <Route path="/" element={<Home/>}/>
              <Route path="/tuner" element={<TunerMetronome/>}/>
              <Route path="/history" element={<PracticeHistory/>}/>
              <Route path="/sheetmusic" element={<SheetMusic/>}/>
              <Route path="/startpracticesession" element={<StartPracticeSession/>}/>
              <Route path="/recording" element={<Recording/>}/>
              <Route path="/performance/:performanceId" element={<Performance/>}/>
            </Routes>
          </BpmContext.Provider>
        </TunerContext.Provider>
      </SheetMusicIdContext.Provider>
    </div>
  );
}

export default App;
