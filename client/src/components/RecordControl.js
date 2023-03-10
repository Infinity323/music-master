import { useContext, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Recorder from 'matt-diamond-recorderjs';
import { baseUrl } from '../App';
import { SheetMusicIdContext } from '../utils/Contexts';
import useMicrophone from '../utils/UseMicrophone';

function RecordControl() {
  const [isRecording, setIsRecording] = useState(false);
  const [isComplete, setIsComplete] = useState(false);
  const [performanceId, setPerformanceId] = useState(-1);

  const sheetMusicId = useContext(SheetMusicIdContext)[0];
  const navigate = useNavigate();
  const stream = useMicrophone();
  
  const audioContext = useRef();
  const recorder = useRef();

  const startRecording = async () => {
    console.log("Starting recording.");
    audioContext.current = new AudioContext();

    console.log("Sample rate: " + audioContext.current.sampleRate);
    console.log("Initializing Recorder.js...");

    let input = audioContext.current.createMediaStreamSource(stream);
    recorder.current = new Recorder(input, {
      numChannels: 1
    })
    recorder.current.record();
    setIsRecording(true);
  }

  const stopRecording = () => {
    console.log("Stopping recording.");
    recorder.current.stop();
    recorder.current.exportWAV(onStop);
    setIsRecording(false);
    setIsComplete(true);
  }

  const cancelRecording = () => {
    console.log("Cancelling recording.");
    recorder.current.stop();
    setIsRecording(false);
    setIsComplete(true);
    navigate(-1);
  }

  const onStop = async (blob) => {
    const formData = new FormData();
    formData.append("sheet_music_id", sheetMusicId);
    formData.append("file", blob);

    await fetch(baseUrl + "/performance", {
      method: "POST",
      body: formData
    }).then((res) => res.json())
      .then((data) => setPerformanceId(data.id))
      .catch(err => console.error(err));
  }

  const viewResults = () => {
    navigate("/performance/" + performanceId);
  }

  return (
    <>
      {
        /* Start recording view */
        !isRecording && !isComplete
          ?
            <>
              <h2>Start Recording</h2>
              <p>Begin playing after the countdown.</p>
              {/* TODO: implement countdown */}
              <div className="btn small" onClick={startRecording}>Start</div>
            </>
          : ""
      }
      {
        /* Recording in progress view */
        isRecording
          ?
            <>
              <h2>Recording in Progress</h2>
              <div className="btn small" onClick={stopRecording}>Stop</div>
              <div className="btn small" onClick={cancelRecording}>Cancel</div>
            </>
          : ""
      }
      {
        /* Recording complete view */
        isComplete
          ?
            <>
              <h2>Recording Complete</h2>
              {
                performanceId !== -1
                  ?
                    <div
                      className="btn medium"
                      onClick={viewResults} 
                      style={{margin: "auto auto"}}
                    >
                      View Results
                    </div>
                  : ""
              }
            </>
          : ""
      }
    </>
  );
}

export default RecordControl;