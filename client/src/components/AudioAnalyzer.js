import { useEffect, useState } from "react";

function AudioAnalyzer(audio) {
  var audioContext, analyzer, dataArray, source, rafId;

  const [audioData, setAudioData] = useState(new Uint8Array(0));

  function tick() {
    analyzer.getByteTimeDomainData(dataArray);
    setAudioData(dataArray);
    rafId = requestAnimationFrame(tick);
  }

  useEffect(() => {
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
    analyzer = audioContext.createAnalyser();
    dataArray = new Uint8Array(analyzer.frequencyBinCount);
    source = audioContext.createMediaStreamSource(audio);
    source.connect(analyzer);
    tick();

    return () => {
      cancelAnimationFrame(rafId);
      analyzer.disconnect();
      source.disconnect();
    }
  }, []);

  return (
    <textarea value={audioData}/>
  );
}

export default AudioAnalyzer;