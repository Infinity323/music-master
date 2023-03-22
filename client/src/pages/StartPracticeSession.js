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
      <div className={sheetMusicId === -1 ? "btn medium disabled" : "btn medium"} onClick={() => navigate("/recording")}>
        <img src={recording} alt="Back" width="60px"/>
      </div>
    );
  }

  return (
    <>
      <BackButton/>
      <div className="content">
        <h1>Practice Session</h1>
        <p>Select the sheet music you want to record a performance of.</p>
        <SheetMusicDropdown/>
        <RecordButton/>
      </div>
    </>
  );
}

export default StartPracticeSession;