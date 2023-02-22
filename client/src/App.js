import { Route, Routes } from 'react-router-dom'
import './App.css';
import Home from './pages/Home';
import PracticeHistory from './pages/PracticeHistory';
import SheetMusic from './pages/SheetMusic';
import StartPracticeSession from './pages/StartPracticeSession';
import Tuner from './pages/Tuner';
import Recording from './pages/Recording';

export const baseUrl = "http://localhost:5000";

export const { style } = document.documentElement;

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Home/>}/>
        <Route path="/tuner" element={<Tuner/>}/>
        <Route path="/history" element={<PracticeHistory/>}/>
        <Route path="/sheetmusic" element={<SheetMusic/>}/>
        <Route path="/startpracticesession" element={<StartPracticeSession/>}/>
        <Route path="/recording" element={<Recording/>}/>
      </Routes>
    </div>
  );
}

export default App;
