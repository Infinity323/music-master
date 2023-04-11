import { HomeButton } from '../components/Buttons';
import Metronome from '../components/Metronome';
import Tuner from '../components/Tuner';

function TunerMetronome() {
  return (
    <>
      <HomeButton/>
      <div className="content">
        <Metronome/>
        <Tuner/>
      </div>
    </>
  );
}

export default TunerMetronome;