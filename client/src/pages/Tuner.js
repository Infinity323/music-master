import { BackButton } from '../components/Buttons';
import { MetronomeButton } from "../components/Metronome";

function Tuner() {
  return(
    <>
      <BackButton/>
      <div className="content">
        <MetronomeButton/>
      </div>
    </>
  );
}

export default Tuner;