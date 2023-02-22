import { BackButton } from "../components/Buttons";
import { RecordButton } from "../components/Buttons";

function StartPracticeSession() {
  return (
    <>
      <BackButton/>
      <div className="content">
        <p>start practice session</p>
        <RecordButton/>
      </div>
    </>
  );
}

export default StartPracticeSession;