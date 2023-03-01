import { useContext, useEffect, useState } from 'react';
import { TunerContext } from '../App';
import AudioAnalyzer from '../utils/AudioAnalyzer';

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
      <div className="tuner-center">
        <text className="tuner-center">
          <text className="note-name">{currentNote ? currentNote.noteName : ""}</text>
          <text>{currentNote ? currentNote.octave : ""}</text>
        </text>
      </div>
      <br/>
      {audio ? <AudioAnalyzer audio={audio}/> : ""}
    </>
  );
}

export default Tuner;