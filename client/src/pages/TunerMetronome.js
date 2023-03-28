import { BackButton } from '../components/Buttons';
import Metronome from '../components/Metronome';
import Tuner from '../components/Tuner';

function TunerMetronome() {
  return (
    <>
      <BackButton/>
      <div className="content">
        <Metronome/>
        <Tuner/>
      </div>
    </>
  );
}

export default TunerMetronome;