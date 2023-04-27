import { useState, useEffect } from 'react';
import { Card } from 'react-bootstrap';
import { log2, abs } from 'mathjs';
import Modal from 'react-modal';
import { baseUrl } from '../App';
import '../assets/css/PerformanceDetails.css';

const NOTE_SYMBOLS = {
  "sixteenth": "𝅘𝅥𝅯",
  "eighth": "♪",
  "quarter": "♩",
  "dotted quarter": "♩.",
  "half": "𝅗𝅥",
  "dotted half": "𝅗𝅥." ,
  "whole": "𝅝",
};

const DIFF_NAMES = {
  "start": "Wrong Start",
  "end": "Wrong End",
  "velocity": "Wrong Volume",
  "pitch": "Wrong Note",
  "extra": "Extra Note",
  "missing": "Missing Note",
};

function frequencyToNoteName(frequency, tolerance = 50) {
  const noteNames = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
  const A4 = 440;
  const A4_MIDI = 69;

  if (frequency <= 0) {
    throw new Error('Frequency must be a positive number.');
  }

  const midiNoteNumber = Math.round(12 * Math.log2(frequency / A4) + A4_MIDI);
  const octave = Math.floor(midiNoteNumber / 12) - 1;
  const noteIndex = midiNoteNumber % 12;
  const noteName = noteNames[noteIndex];

  const idealFrequency = A4 * Math.pow(2, (midiNoteNumber - A4_MIDI) / 12);
  const centsDifference = 1200 * Math.log2(frequency / idealFrequency);

  if (Math.abs(centsDifference) <= tolerance) {
    return noteName + octave;
  } else {
    const sharpOrFlat = centsDifference > 0 ? '♯' : '♭';
    const cents = Math.abs(Math.round(centsDifference));
    return `${noteName}${octave}${sharpOrFlat}${cents}`;
  }
}

function PerformanceDetails({ sheet_music_id, run_number }) {
  const [performanceDiffs, setPerformanceDiffs] = useState([]);
  const [measureGroups, setMeasureGroups] = useState([]);
  const [modalIsOpen, setModalIsOpen] = useState(false);

  useEffect(() => {
    const loadDiffData = async () => {
      try {
        const response = await fetch(baseUrl + `/performance/diff/${sheet_music_id}/${run_number}`);

        if (!response.ok) {
          throw new Error(`Error fetching diff data: ${response.statusText}`);
        }

        const data = await response.json();
        setPerformanceDiffs(data);
        let tempMeasures = [];
        data.forEach(diff => {
          if (tempMeasures[diff.note_info.measure]) {
            tempMeasures[diff.note_info.measure].push(diff);
          } else if (diff.diff.diff_type === "extra") {
            if (tempMeasures[diff.note_info[0].measure])
              tempMeasures[diff.note_info[0].measure].push(diff);
            else
              tempMeasures[diff.note_info.measure] = [diff];
          } else {
            tempMeasures[diff.note_info.measure] = [diff];
          }
        });
        setMeasureGroups(tempMeasures);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    loadDiffData();
  }, [sheet_music_id, run_number]);

  const renderDiff = (diff) => {
    const { ideal_val, actual_val, diff_type } = diff.diff;
    const valueLabels = {
      pitch: 'Pitch',
      velocity: 'Velocity',
      start: 'Start',
      end: 'End',
    };

    if (diff_type === 'pitch') {
      // calculate pitch difference in cents
      const pitch_difference = 1200 * log2(actual_val[diff_type] / ideal_val[diff_type]);
      let description = "";

      if (pitch_difference < 0) {
        description = "flat"
      } else {
        description = "sharp"
      }

      return (
        <>
          You played {frequencyToNoteName(actual_val[diff_type])} instead of {diff.note_info.name}.
          ({abs(pitch_difference).toFixed(0)} cents {description})
        </>
      );

    }

    if (diff_type === 'velocity') {
      const difference = actual_val[diff_type].toFixed(0) - ideal_val[diff_type].toFixed(0);
      const percentageDifference = (abs(difference) / ideal_val[diff_type].toFixed(0)) * 100;
      if (ideal_val[diff_type].toFixed(0) > actual_val[diff_type].toFixed(0)) {
        // Too quiet
        return (
          <>
            { percentageDifference < 50
              ? "You played a little too quietly here."
              : "You played too quietly here."
            }
          </>
        );
      } else {
        // Too loud
        return (
          <>
            { percentageDifference < 50
              ? "You played a little too loudly here."
              : "You played too loudly here."
            }
          </>
        );
      }
    }

    if (diff_type === 'start') {
      const difference = abs(actual_val[diff_type] - ideal_val[diff_type]);
      if (ideal_val[diff_type] > actual_val[diff_type]) {
        return (
          <>You started the note too early. ({difference.toFixed(2)} s)</>
        );
      } else {
        return (
          <>You started the note too late. ({difference.toFixed(2)} s)</>
        );
      }
    }

    if (diff_type === 'end') {
      const difference = abs(actual_val[diff_type] - ideal_val[diff_type]);
      if (ideal_val[diff_type] > actual_val[diff_type]) {
        return (
          <>You ended the note too early. ({difference.toFixed(2)} s)</>
        );
      } else {
        return (
          <>You ended the note too late. ({difference.toFixed(2)} s)</>
        );
      }
    }

    if (diff_type === 'missing') {
      return <>Note is missing.</>;
    }

    if (diff_type === 'extra') {
      return (
        <>You played an extra note. ({frequencyToNoteName(actual_val["pitch"])})</>
      );
    }

    return (
      <>
        Ideal: {valueLabels[diff_type]} {ideal_val[diff_type].toFixed(2)}
        <br />
        Actual: {valueLabels[diff_type]} {actual_val[diff_type].toFixed(2)}
      </>
    );
  };

  const renderSubtitle = (diff) => {
    const { diff_type } = diff.diff;
    const description = diff.description;
    const note_info = diff.note_info;

    if (diff_type === 'extra') {
      return (
        <Card.Subtitle className="mb-2 text-muted cardSubtitle">
          { description === "Between"
            ? `Extra note detected between ${note_info[0].name} and ${note_info[1].name}`
            : description === "Before"
              ? `Extra note detected before ${note_info[0].name}`
              : `Extra note detected after ${note_info[0].name}`
          }
        </Card.Subtitle>
      );
    }

    return (
      <Card.Subtitle className="mb-2 text-muted cardSubtitle">
        {`Note ${note_info.position}, ${note_info.name.replace('-', '♭')} (${NOTE_SYMBOLS[note_info.type]})`}
      </Card.Subtitle>
    );
  };

  function openModal() {
    setModalIsOpen(true);
  }
  function closeModal() {
    setModalIsOpen(false);
  }

  if (performanceDiffs.length)
    return (
      <>
        <div className="btn small" onClick={openModal}>
          Differences
        </div>
        <Modal isOpen={modalIsOpen} onRequestClose={closeModal} className="modal" overlayClassName="modal-overlay">
          <h3>Differences Found</h3>
          { measureGroups.map((measure, index) => (
            <>
              Measure {index}
              <div className="cardGroup">
                { measure.map((diff, index) => (
                    <Card className="customCard">
                      <Card.Body>
                        <Card.Title className="cardTitle">
                          {index + 1}. {DIFF_NAMES[diff.diff.diff_type]}
                        </Card.Title>
                        {renderSubtitle(diff)}
                        <Card.Text className="cardText">
                          {renderDiff(diff)}
                        </Card.Text>
                      </Card.Body>
                    </Card>
                  ))
                }
              </div>
            </>
          ))}
          <div className="btn medium" onClick={closeModal}>Close</div>
        </Modal>
      </>
    );
}

export default PerformanceDetails;
