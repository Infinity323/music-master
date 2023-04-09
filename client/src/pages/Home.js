import { useNavigate } from "react-router-dom";
import { ThemeButton } from "../components/Buttons";

function Home() {
  const navigate = useNavigate();

  return(
    <>
      <ThemeButton/>
      <div className="content">
        <h1 className="title">Music Master</h1>
        <div className="btn menu" onClick={() => navigate("/tuner")}>Tuner/Metronome</div>
        <div className="btn menu" onClick={() => navigate("/startpracticesession")}>Start Practice Session</div>
        <div className="btn menu" onClick={() => navigate("/history")}>View Practice History</div>
        <div className="btn menu" onClick={() => navigate("/sheetmusic")}>View Sheet Music</div>
      </div>
    </>
  );
}

export default Home;