import { HomeButton } from "../components/Buttons";
import SheetMusicDropdown from "../components/SheetMusicDropdown";
import PracticeHistoryGraph from "../components/PracticeHistoryGraph";

function PracticeHistory() {
  return (
    <>
      <HomeButton/>
      <div className="content">
        <h2>Practice History</h2>
        <SheetMusicDropdown/>
        <PracticeHistoryGraph/>
      </div>
    </>
  );
}

export default PracticeHistory;