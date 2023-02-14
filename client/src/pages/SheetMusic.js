import { BackButton } from "../components/Buttons";
import SheetMusicTable from "../components/SheetMusicTable";

function SheetMusic() {
  return (
    <>
      <BackButton/>
      <div className="content">
        <SheetMusicTable/>
      </div>
    </>
  );
}

export default SheetMusic;