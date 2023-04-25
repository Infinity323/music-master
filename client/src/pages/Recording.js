import { BackButton } from "../components/Buttons";
import RecordControl from "../components/RecordControl";
import MetronomeRecording from "../components/MetronomeRecording";

function Recording() {
  return (
    <>
      <BackButton/>
      <div className="content">
        <RecordControl/>
      </div>
    </>
  );
}

export default Recording;