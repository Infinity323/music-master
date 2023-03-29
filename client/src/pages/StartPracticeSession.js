import { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { BackButton } from '../components/Buttons';
import SheetMusicDropdown from '../components/SheetMusicDropdown';
import { SheetMusicIdContext } from '../utils/Contexts';
import BpmSelector from "../components/BpmSelector";

function StartPracticeSession() {

  function RecordButton() {
    const navigate = useNavigate();
    const sheetMusicId  = useContext(SheetMusicIdContext)[0];

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
      <BackButton/>
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