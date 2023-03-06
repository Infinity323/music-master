import { BackButton } from "../components/Buttons";
import SheetMusicDropdown from "../components/SheetMusicDropdown";
import { useNavigate } from 'react-router-dom';
import { useContext } from "react";
import { SheetMusicIdContext } from "../App";
import recording from '../assets/images/recording.png'

function StartPracticeSession() {

  function RecordButton() {
    const navigate = useNavigate();
    const sheetMusicId  = useContext(SheetMusicIdContext)[0];
    return (
      <div
        className={sheetMusicId === -1 ? "btn medium disabled" : "btn medium"}
        onClick={() => navigate("/recording")}
        style={{
          margin:"auto auto"
        }}
      >
        <img src={recording} alt="Back" width="80px"/>
      </div>
    );
  }

  return (
    <>
      <BackButton/>
      <div className="content">
        <h2>Start Practice Session</h2>
        <p>Select which piece you would like to practice.</p>
        <div style={{display: "flex", justifyContent: "center", margin: "20px"}}>
          <SheetMusicDropdown/>
        </div>
        <RecordButton/>
      </div>
    </>
  );
}

export default StartPracticeSession;