import { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { HomeButton } from '../components/Buttons';
import SheetMusicDropdown from '../components/SheetMusicDropdown';
import { SheetMusicContext } from '../utils/Contexts';
import BpmSelector from "../components/BpmSelector";

function StartPracticeSession() {

  function RecordButton() {
    const navigate = useNavigate();
    const sheetMusicId  = useContext(SheetMusicContext)[0].id;

    return (
      <div
        className={sheetMusicId === -1 ? "btn medium disabled" : "btn medium"}
        onClick={() => navigate("/recording")}
        style={{margin: "auto auto"}}
      >
        Continue
      </div>
    );
  }

  return (
    <>
      <HomeButton/>
      <div className="content">
        <h2>Start Practice Session</h2>
        <p>Select the piece to practice.</p>
        <div style={{display: "flex", justifyContent: "center", margin: "20px"}}>
          <SheetMusicDropdown/>
        </div>
        <p>Select the tempo to practice at.</p>
        <BpmSelector/>
        <RecordButton/>
      </div>
    </>
  );
}

export default StartPracticeSession;