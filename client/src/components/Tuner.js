import { useContext, useEffect, useRef, useState } from 'react';
import { IgrLinearGauge, IgrLinearGaugeModule } from 'igniteui-react-gauges';
import { TunerContext } from '../App';
import AudioAnalyzer from '../utils/AudioAnalyzer';
import useMicrophone from '../utils/UseMicrophone';
import { style } from '../App';

IgrLinearGaugeModule.register();

function Tuner() {
  const textColor = style.getPropertyValue('--text-color');
  const btnColor = style.getPropertyValue('--btn-color');
  const hoverColor = style.getPropertyValue('--hover-color');

  const microphone = useMicrophone();
  const currentNote = useContext(TunerContext)[0];

  return (
    <>
      <div className="tuner-center">
        <text className="tuner-center">
          <text className="note-name">{currentNote ? currentNote.noteName : ""}</text>
          <text>{currentNote ? currentNote.octave : ""}</text>
        </text>
      </div>
      <br/>
      <div className="tuner-gauge">
        <IgrLinearGauge
          height="60px"
          minimumValue={-50}
          maximumValue={50}
          interval={10}
          tickBrush={textColor}
          tickStrokeThickness={1}
          labelInterval={10}
          labelExtent={0.025}
          labelsPreTerminal={0}
          labelsPostInitial={0}
          font="11px Segoe UI"
          value={currentNote.cents}
          isNeedleDraggingEnabled={true}
          needleBrush={hoverColor}
          needleOutline={textColor}
          needleStrokeThickness={1}
          backingBrush={btnColor}
          backingOutline={"rgba(1, 1, 1, 0.5)"}
          backingStrokeThickness={1}
        />
      </div>
      {microphone ? <AudioAnalyzer audio={microphone} /> : ""}
    </>
  );
}

export default Tuner;