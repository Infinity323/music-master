import { BackButton } from '../components/Buttons';
import { MetronomeButton } from '../components/Metronome';
import Tuner from '../components/Tuner';

function TunerMetronome() {
  return (
    <>
      <BackButton/>
      <div className="content">
        <MetronomeButton/>
        <Tuner/>
      </div>
    </>
  );
}

export default TunerMetronome;