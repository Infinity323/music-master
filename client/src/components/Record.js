import '../App.css';
import axios from "axios";

let gumStream = null;
let recorder = null;
let audioContext = null;

function RecorderJSDemo() {

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

                recorder = new window.Recorder(input, {
                    numChannels: 1
                })

                recorder.record();
                console.log("Recording started");
            }).catch(function (err) {
                //enable the record button if getUserMedia() fails
        });

    }

    const stopRecording = () => {
        console.log("stopButton clicked");

        recorder.stop(); //stop microphone access
        gumStream.getAudioTracks()[0].stop();

        recorder.exportWAV(onStop);
    }

    const onStop = (blob) => {
        console.log("uploading...");

        let data = new FormData();

        data.append('text', "this is the transcription of the audio file");
        data.append('wavfile', blob, "recording.wav");

        const config = {
            headers: {'content-type': 'multipart/form-data'}
        }
        axios.post('http://localhost:5000/record/', data, config);
    }

    return (
        <div>
            <button onClick={startRecording} type="button">Start</button>
            <button onClick={stopRecording} type="button">Stop</button>
        </div>
    );
}

export default RecorderJSDemo;