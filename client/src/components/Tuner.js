import { useContext, useEffect, useState } from 'react';
import { TunerContext } from '../App';
import AudioAnalyzer from './AudioAnalyzer';

function Tuner() {
  const [audio, setAudio] = useState(null);
  const currentNote = useContext(TunerContext)[0];

  async function getMicrophone() {
    const media = await navigator.mediaDevices.getUserMedia({
      audio: true,
      video: false
    });
    setAudio(media);
  }

  useEffect(() => {
    getMicrophone();

    return () => {
      if (audio)
        audio.getTracks().forEach(track => track.stop());
    };
  }, []);

  return (
    <>
      {currentNote}
      {audio ? <AudioAnalyzer audio={audio}/> : ''}
    </>
  );
}

export default Tuner;