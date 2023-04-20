import { useContext, useEffect } from 'react';
import { BpmContext, SheetMusicContext } from '../utils/Contexts';

function BpmSelector() {
  const [bpm, setBpm] = useContext(BpmContext);
  const defaultTempo = useContext(SheetMusicContext)[0].tempo;

  function increaseBpm() {
    // Max tempo is 240
    setBpm(bpm === 240 ? bpm : bpm + 10);
  }

  function decreaseBpm() {
    // Min tempo is 10
    setBpm(bpm === 10 ? bpm : bpm - 10);
  }
  
  useEffect(() => {
    // Default tempo is ideal sheet music tempo
    if (defaultTempo)
      setBpm(defaultTempo);
  }, [defaultTempo]);

  return (
    <div style={{margin: 10}}>
      <div className="btn bpm" onClick={decreaseBpm}>-</div>
      {` ${bpm} `}
      <div className="btn bpm" onClick={increaseBpm}>+</div>
    </div>
  );
}

export default BpmSelector;