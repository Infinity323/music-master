import { HomeButton } from "../components/Buttons";
import SheetMusicTable from "../components/SheetMusicTable";

function SheetMusic() {
  return (
    <>
      <HomeButton/>
      <div className="content">
        <h2>Sheet Music</h2>
        <SheetMusicTable/>
      </div>
    </>
  );
}

export default SheetMusic;