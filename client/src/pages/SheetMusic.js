import { BackButton } from "../components/Buttons";
import SheetMusicTable from "../components/SheetMusicTable";

function SheetMusic() {
  return (
    <>
      <BackButton/>
      <div className="content">
        <h2>Sheet Music</h2>
        <SheetMusicTable/>
      </div>
    </>
  );
}

export default SheetMusic;