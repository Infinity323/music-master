import { Route, Routes } from 'react-router-dom'
import './App.css';
import Home from './pages/Home';
import SheetMusic from './pages/SheetMusic';
import Tuner from './pages/Tuner';

export const baseUrl = "http://localhost:5000";

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Home/>}/>
        <Route path="/tuner" element={<Tuner/>}/>
        <Route path="/sheetmusic" element={<SheetMusic/>}/>
      </Routes>
    </div>
  );
}

export default App;
