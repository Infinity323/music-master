import { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import Recorder from 'matt-diamond-recorderjs';
import { baseUrl } from '../App';
import { SheetMusicIdContext } from '../utils/Contexts';

let gumStream = null;
let recorder = null;
let audioContext = null;

function Record() {

    const sheetMusicId  = useContext(SheetMusicIdContext)[0];
    const navigate = useNavigate();

    const startRecording = () => {
        let constraints = {
            audio: true,
            video: false
        }

        audioContext = new window.AudioContext();
        console.log("sample rate: " + audioContext.sampleRate);

        navigator.mediaDevices
            .getUserMedia(constraints)
            .then(function (stream) {
                console.log("initializing Recorder.js ...");

                gumStream = stream;

                let input = audioContext.createMediaStreamSource(stream);

                recorder = new Recorder(input, {
                    numChannels: 1
                })

                recorder.record();
                console.log("Recording started");
            }).catch(function (err) {
                console.log(err)
                // enable the record button if getUserMedia() fails
        });

    }

    const stopRecording = () => {
        console.log("stopButton clicked");

        recorder.stop(); //stop microphone access
        gumStream.getAudioTracks()[0].stop();

        recorder.exportWAV(onStop);

        navigate(-1);
    }

    const onStop = (blob) => {
        console.log("uploading...");

        const formData = new FormData();
        formData.append("sheet_music_id", sheetMusicId);
        formData.append("file", blob);
        
        fetch(baseUrl + "/performance", {
            method: "POST",
            body: formData
        }).then(res => {
            console.log("Success: " + res.data);
        })
        .catch(err => {
            console.log(err);
        })
    }

    return (
        <div>  
            <p>start/stop recorind for music sheet: {sheetMusicId}</p>
            <button onClick={startRecording} type="button">Start</button>
            <button onClick={stopRecording} type="button">Stop</button>
            <button onClick={() => {navigate(-1)}} type="button">Cancel</button>
        </div>
    );
}

export default Record;