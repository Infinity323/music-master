import { useContext, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Recorder from 'matt-diamond-recorderjs';
import { baseUrl } from '../App';
import { BpmContext, SheetMusicContext } from '../utils/Contexts';
import useMicrophone from '../utils/UseMicrophone';
import loading_gif from '../assets/images/loading_gif.gif'
import MetronomeRecording from './MetronomeRecording';

function RecordControl() {
  const [isRecording, setIsRecording] = useState(false);
  const [isComplete, setIsComplete] = useState(false);
  const [isStarting, setIsStarting] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [performanceId, setPerformanceId] = useState(-1);
  const [countdownDisplay, setCountdownDisplay] = useState(10);
  const inputRef = useRef();

  const sheetMusicId = useContext(SheetMusicContext)[0].id;
  const bpm = useContext(BpmContext)[0];
  const navigate = useNavigate();
  const stream = useMicrophone();
  
  const audioContext = useRef();
  const recorder = useRef();

  const startCountdown = () => {
    // Countdown speed matches set BPM
    let msPerBeat = 1.0/bpm*60.0*1000.0;
    // Longer countdown for faster BPM's
    let countdownStart = bpm >= 120 ? 10 : 6;
    setCountdownDisplay(countdownStart)

    return new Promise((resolve, reject) => {
      let localCountdownNumber = countdownStart;
      const timerId = setInterval(() => {
        setCountdownDisplay(--localCountdownNumber);
        if (localCountdownNumber === 0) {
          clearInterval(timerId);
          resolve();
        }
      }, msPerBeat);
    });
  }

  const startRecording = async () => {
    // Wait for countdown
    // setIsStarting(true);
    // await startCountdown();
    setIsStarting(false);

    // Then start recording
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

  const uploadPrerecorded = (file) => {
    onStop(file).then(() => {
      setIsRecording(false);
      setIsComplete(true);
    });
  }

  const onStop = async (blob) => {
    const formData = new FormData();
    formData.append("sheet_music_id", sheetMusicId);
    formData.append("average_tempo", bpm);
    formData.append("file", blob);

    setIsLoading(true);
    await fetch(baseUrl + "/performance", {
      method: "POST",
      body: formData
    }).then((res) => res.json())
      .then((data) => setPerformanceId(data.id))
      .catch(err => console.error(err));
    setIsLoading(false);
  }

  const viewResults = () => {
    navigate("/performance/" + performanceId);
  }

  return (
    <>
      { /* Start recording view */
        !isRecording && !isComplete
        ? <>
            <h2>Start Recording</h2>
            <p>Start a new live recording or upload an existing one.</p>
            <div
              className={isLoading ? "btn small disabled" : "btn small"}
              onClick={startRecording}
            >
              Start
            </div>
          </>
        : ""
      }
      { /* Upload button */
        !isStarting && !isRecording && !isComplete
        ? <>
            <p>or</p>
            <label
              className={isLoading ? "btn small disabled" : "btn small"}
              style={{width: 200}}
            >
              {isLoading ? "Uploading..." : "Upload a Recording"}
              <input
                type="file"
                accept=".wav"
                onChange={() => {uploadPrerecorded(inputRef.current.files[0])}}
                ref={inputRef}/>
            </label>
          </>
        : ""
      }
      { /* Countdown */
        // isStarting
        // ? <div className="countdown">
        //     {"" + countdownDisplay}
        //   </div>
        // : ""
      }
      { /* Recording in progress view */
        isRecording
        ? <>
            <h2>Recording in Progress</h2>
            <p>Begin playing whenever ready.</p>
            <MetronomeRecording bpm={bpm}/>
            <div className="btn small" onClick={stopRecording}>Stop</div>
            <div className="btn small" onClick={cancelRecording}>Cancel</div>
          </>
        : ""
      }
      { /* Recording complete view */
        isComplete
        ? <>
            <h2>Recording Complete</h2>
            { performanceId !== -1
              ? <div
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
      { /* Loading gif */
        isLoading
        ? <div style={{margin:30}}>
            <img src={loading_gif} width="40px" alt="Loading..."/>
          </div>
        : ""
      }
    </>
  );
}

export default RecordControl;