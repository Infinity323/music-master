import { useContext } from 'react';
import { BpmContext } from '../utils/Contexts';

function BpmSelector() {
  const [bpm, setBpm] = useContext(BpmContext);

  const increaseBpm = () => {
    setBpm(bpm === 240 ? bpm : bpm + 10);
  }

  const decreaseBpm = () => {
    setBpm(bpm === 10 ? bpm : bpm - 10);
  }

  return (
    <div style={{margin: 10}}>
      <div className="btn bpm" onClick={decreaseBpm}>-</div>
      {" " + bpm + " "}
      <div className="btn bpm" onClick={increaseBpm}>+</div>
    </div>
  );
}

export default BpmSelector;