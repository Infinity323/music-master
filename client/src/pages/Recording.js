import { BackButton } from "../components/Buttons";
import RecordControl from "../components/RecordControl";
import MetronomeRecording from "../components/MetronomeRecording";
import Metronome from "../components/Metronome";

function Recording() {
  return (
    <>
      <BackButton/>
      <div className="content">
        <RecordControl/>
        <div className="metrorecalign">
        <MetronomeRecording></MetronomeRecording>
      </div>
      </div>
    </>
  );
}

export default Recording;