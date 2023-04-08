import { useContext } from 'react';
import { IgrLinearGauge, IgrLinearGaugeModule, IgrLinearGraphRange } from 'igniteui-react-gauges';
import { TunerContext } from '../utils/Contexts';
import AudioAnalyzer from '../utils/AudioAnalyzer';
import useMicrophone from '../utils/UseMicrophone';
import { style } from '../App';

IgrLinearGaugeModule.register();

function Tuner() {
  const textColor = style.getPropertyValue('--text-color');
  const btnColor = style.getPropertyValue('--btn-color');
  const selectColor = style.getPropertyValue('--select-color');
  const borderColor = "rgba(1, 1, 1, 0.2)";

  const microphone = useMicrophone();
  const currentNote = useContext(TunerContext)[0];

  return (
    <>
      <div className="tuner-center">
        <text className="tuner-center">
          <text className="note-name">{currentNote ? currentNote.noteName : ""}</text>
          <text>{currentNote ? currentNote.octave : ""}</text>
          <br/>
          <text className="freq">{currentNote.freq ? Math.round(currentNote.freq*100)/100 + " Hz" : ""}</text>
        </text>
      </div>
      <br/>
      <div className="tuner-gauge">
        <IgrLinearGauge
          height="60px"
          minimumValue={-50}
          maximumValue={50}
          interval={10}
          tickBrush={borderColor}
          tickStrokeThickness={1}
          tickEndExtent={0.5}
          labelInterval={10}
          labelExtent={0.025}
          labelsPreTerminal={0}
          labelsPostInitial={0}
          font="11px AppleRegular"
          value={currentNote.cents ? currentNote.cents : 0}
          isNeedleDraggingEnabled={true}
          needleBrush={selectColor}
          needleOutline={textColor}
          needleStrokeThickness={0.5}
          backingBrush={btnColor}
          backingOutline=""
          backingStrokeThickness={0}
          transitionDuration={200}
          rangeBrushes={"#E81F1F, #E89F1F, #E8D91F, #93E81F, #62E81F, #93E81F, #E8D91F, #E89F1F, #E81F1F"}
        >
          <IgrLinearGraphRange
            name="bad-left"
            startValue={-50} endValue={-45}
          />
          <IgrLinearGraphRange
            name="worse-left"
            startValue={-45} endValue={-30}
          />
          <IgrLinearGraphRange
            name="ok-left"
            startValue={-30} endValue={-15}
          />
          <IgrLinearGraphRange
            name="alright-left"
            startValue={-15} endValue={-10}
          />
          <IgrLinearGraphRange
            name="good"
            startValue={-10} endValue={10}
          />
          <IgrLinearGraphRange
            name="alright-right"
            startValue={10} endValue={15}
          />
          <IgrLinearGraphRange
            name="ok-right"
            startValue={15} endValue={30}
          />
          <IgrLinearGraphRange
            name="worse-right"
            startValue={30} endValue={45}
          />
          <IgrLinearGraphRange
            name="bad-right"
            startValue={45} endValue={50}
          />
        </IgrLinearGauge>
      </div>
      {microphone ? <AudioAnalyzer audio={microphone} /> : ""}
    </>
  );
}

export default Tuner;