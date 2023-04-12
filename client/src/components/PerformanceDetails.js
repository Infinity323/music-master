import { useState, useEffect } from 'react';
import { Card, Container, Row, Col } from 'react-bootstrap';
import { baseUrl } from '../App';
import '../assets/css/PerformanceDetails.css'
import { log2, abs } from 'mathjs'

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

  useEffect(() => {
    const loadDiffData = async () => {
      try {
        const response = await fetch(baseUrl + `/performance/diff/${sheet_music_id}/${run_number}`);

        if (!response.ok) {
          throw new Error(`Error fetching diff data: ${response.statusText}`);
        }

        const data = await response.json();
        setPerformanceDiffs(data);
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

    if (diff_type == 'pitch') {
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
            You were {abs(pitch_difference).toFixed(0)} cents {description}.
            <br/>
            You played {frequencyToNoteName(actual_val[diff_type])} instead of {diff.note_info.name}
            </>
        );

    }

    if (diff_type === 'velocity') {
        const difference = actual_val[diff_type].toFixed(0) - ideal_val[diff_type].toFixed(0);
        const percentageDifference = (abs(difference) / ideal_val[diff_type].toFixed(0)) * 100;
        if (ideal_val[diff_type].toFixed(0) > actual_val[diff_type].toFixed(0)) {
            return (
                <>
                Consider increasing dynamic by {percentageDifference.toFixed(0)}% here.
                </>
            );
        } else  {
            return (
                <>
                Consider decreasing dynamic by {percentageDifference.toFixed(0)}% here.
                </>
            );
        }
    }

    if (diff_type === 'start') {
        const difference = abs(actual_val[diff_type] - ideal_val[diff_type]);
        if (ideal_val[diff_type] > actual_val[diff_type]) {
            return (
                <>
                Started note too soon, by {difference.toFixed(2)} seconds.
                </>
            );
        } else  {
            return (
                <>
                Started note too late, by {difference.toFixed(2)} seconds.
                </>
            );
        }
    }

    if (diff_type === 'end') {
        const difference = abs(actual_val[diff_type] - ideal_val[diff_type]);
        if (ideal_val[diff_type] > actual_val[diff_type]) {
            return (
                <>
                Ended note too soon, by {difference.toFixed(2)} seconds.
                </>
            );
        } else  {
            return (
                <>
                Ended note too late, by {difference.toFixed(2)} seconds.
                </>
            );
        }
    }

    if (diff_type === 'missing') {
        return <span>Note is {diff_type}.</span>;
    }

    if (diff_type === 'extra') {
        return (
          <div>
            {diff.note_info.map((info, index) => (
              <span key={index}>
                {info.name} ({info.type}) in Measure {info.measure}, Note #{info.position}
                <br/>
              </span>
            ))}
          </div>
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
    if (diff.diff.diff_type === 'extra') {
      return (
        <Card.Subtitle className="mb-2 text-muted cardSubtitle">
          Extra Note Detected {diff.description}
        </Card.Subtitle>
      );
    }

    return (
      <Card.Subtitle className="mb-2 text-muted cardSubtitle">
        {diff.note_info.name} ({diff.note_info.type}) in Measure {diff.note_info.measure}, Note #{diff.note_info.position}
      </Card.Subtitle>
    );
  };

  return (
    <div>
        <h1>Differences Found</h1>
        <div className="cardStack">
                {performanceDiffs.map((diff, index) => (
                    <div className="cardWrapper">
                        <Card className="customCard">
                        <Card.Body>
                            <Card.Title className="cardTitle">Difference {index + 1} {"(" + diff.diff.diff_type + ")"} </Card.Title>
                            {renderSubtitle(diff)}
                            <Card.Text className="cardText">
                            {renderDiff(diff)}
                            </Card.Text>
                        </Card.Body>
                        </Card>
                    </div>
                ))}
        </div>
    </div>
  );
}

export default PerformanceDetails;
