import { BackButton } from "../components/Buttons";
import RecordControl from "../components/RecordControl";

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