// https://github.com/mrRodrigo/React-Guitar-Tuner/blob/master/src/utils/note-analyzer/index.js
import { useContext, useEffect, useState } from 'react';
import Pitchfinder from 'pitchfinder';
import { TunerContext } from '../App';

const A = 440;
const SEMITONE = 69;
const noteStrings = [
  "C",
  "C♯",
  "D",
  "D♯",
  "E",
  "F",
  "F♯",
  "G",
  "G♯",
  "A",
  "A♯",
  "B"
];

const getNote = freq => {
  const note = 12 * (Math.log(freq / A) / Math.log(2));
  return Math.round(note) + SEMITONE;
};

const getStandardFrequency = note => {
  return A * Math.pow(2, (note - SEMITONE) / 12);
};

const getCents = (frequency, note) => {
  return Math.floor(
    (1200 * Math.log(frequency / getStandardFrequency(note))) / Math.log(2)
  );
};

function AudioAnalyzer({audio}) {
  var audioContext, analyzer, dataArray, dataArray32, source, rafId;
  const detectPitch = new Pitchfinder.AMDF({
    maxFrequency: 800,
    minFrequency: 50
  });

  const setCurrentNote = useContext(TunerContext)[1];

  function tick() {
    dataArray32 = new Float32Array(analyzer.fftSize);
    analyzer.getFloatTimeDomainData(dataArray32);
    const pitch = detectPitch(dataArray32);
    if (pitch) {
      const freq = pitch * 1.09;
      const note = getNote(freq);
      const cents = getCents(freq, note);
      const noteName = noteStrings[note % 12];
      const octave = parseInt(note / 12) - 1;
      setCurrentNote({freq, cents, noteName, octave});
    }
    rafId = requestAnimationFrame(tick);
  }

  useEffect(() => {
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
    analyzer = audioContext.createAnalyser();
    dataArray = new Uint8Array(analyzer.frequencyBinCount);
    source = audioContext.createMediaStreamSource(audio);
    source.connect(analyzer);
    rafId = requestAnimationFrame(tick);

    return () => {
      cancelAnimationFrame(rafId);
      analyzer.disconnect();
      source.disconnect();
    }
  }, []);

  return;
}

export default AudioAnalyzer;