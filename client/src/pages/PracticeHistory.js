import { BackButton } from "../components/Buttons";
import SheetMusicDropdown from "../components/SheetMusicDropdown";

function PracticeHistory() {
  return (
    <>
      <BackButton/>
      <div className="content">
        <SheetMusicDropdown/>
      </div>
    </>
  );
}

export default PracticeHistory;