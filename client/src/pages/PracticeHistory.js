import { BackButton } from "../components/Buttons";
import PracticeHistoryGraph from "../components/PracticeHistoryGraph";
import SheetMusicDropdown from "../components/SheetMusicDropdown";

function PracticeHistory() {
  return (
    <>
      <BackButton/>
      <div className="content">
        <SheetMusicDropdown/>
        <PracticeHistoryGraph/>
      </div>
    </>
  );
}

export default PracticeHistory;