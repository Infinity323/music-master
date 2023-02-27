import { BackButton } from "../components/Buttons";
import SheetMusicDropdown from "../components/SheetMusicDropdown";
import PracticeHistoryGraph from "../components/PracticeHistoryGraph";

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