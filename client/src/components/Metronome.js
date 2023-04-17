import React, { Component } from 'react';
import image_metronome from '../assets/images/metronome.png';
import image_metronome_white from '../assets/images/metronome_white.png';
import { Flex, Box, CircularProgress, CircularProgressLabel, Button } from '@chakra-ui/react';
import { ThemeContext } from '../utils/Contexts';
/*
//Circle
//https://medium.com/tinyso/how-to-create-an-animated-svg-circular-progress-component-in-react-5123c7d24391
const Circular = ({size,strokeWidth,percentage,color}) => {
  const viewBox = '0 0 ${size} ${size}';
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * Math.PI *2;
  const dash = (percentage*circumference) / 100;
  return(
    <svg width={size} height={size} viewBox={viewBox}>
      <circle
        fill="none"
        stroke="#ccc"
        cx={size / 2}
        cy={size / 2}
        r={radius}
        strokeWidth={'${strokeWidth}px'}
      />
      <circle
        fill="none"
        strokeWidth={color}
        cx={size / 2}
        cy={size / 2}
        r={radius}
        strokeWidth={'${strokeWidth}px'}
        transform={'rotate(-90 ${size / 2} ${size / 2})'}
        strokeDasharray={[dash,circumference - dash]}
        strokeLinecap="round"
      />
    </svg>
  );
}*/

// Metronome built using this as guidance.
// https://grantjam.es/creating-a-simple-metronome-using-javascript-and-the-web-audio-api/
class Metronome extends Component {
  constructor(props) {
    super(props);

    this.audioContext = React.createRef();
    this.audioContext.current = null;
    
    this.state = {
      // User-customizable state variables
      currentBeatInBar: 0,
      beatsPerBar: 4,
      bpm: 100,
      btn3: true,
      btn4: true,
      btn5: false,
      btn6: false,
      lastbeat: false,
      // Internal state variables
      lookahead: 25,
      scheduleAheadTime: 0.1,
      nextNoteTime: 0.0,
      timerID: null,
      isPlaying: false,
      isBeat: false
    };
  }

  chgbtn3 = () => {
    if(this.state.btn3 === false){
      this.setState(state => ({
        btn3: true,
        beatsPerBar: 3
      }));
    }
    else{
      this.setState(state => ({
        btn3: false,
        btn4: false,
        btn5: false,
        btn6: false,
        beatsPerBar: 2
      }));
    }
  }
  chgbtn4 = () => {
    if(this.state.btn4 === false){
      this.setState(state => ({
        btn3: true,
        btn4: true,
        beatsPerBar: 4
      }));
    }
    else{
      this.setState(state => ({
        btn4: false,
        btn5: false,
        btn6: false,
        beatsPerBar: 3
      }));
    }
  }
  chgbtn5 = () => {
    if(this.state.btn5 === false){
      this.setState(state => ({
        btn3: true,
        btn4: true,
        btn5: true,
        beatsPerBar: 5
      }));
    }
    else{
      this.setState(state => ({
        btn5: false,
        btn6: false,
        beatsPerBar: 4
      }));
    }
  }
  chgbtn6 = () => {
    if(this.state.btn6 === false){
      this.setState(state => ({
        btn3: true,
        btn4: true,
        btn5: true,
        btn6: true,
        beatsPerBar: 6
      }));
    }
    else{
      this.setState(state => ({
        btn6: false,
        beatsPerBar: 5
      }));
    }
  }

  /**
   * Increments the next note time and current beat in bar.
   * Adjusts seconds per beat in case metronome was adjusted.
   */
  nextBeat = () => {
    var secondsPerBeat = 60.0 / this.state.bpm;
    this.setState(state => ({
      nextNoteTime: state.nextNoteTime + secondsPerBeat,
      currentBeatInBar: (state.currentBeatInBar + 1) % state.beatsPerBar
    }));
  }

  /**
   * Schedules next metronome beat.
   * Creates oscillator to produce the beat sound.
   * @param {number} beatNumber The beat number in the bar.
   * @param {number} time The time to schedule the beat sound.
   */
  scheduleBeat = (beatNumber, time) => {
    const osc = this.audioContext.current.createOscillator();
    const envelope = this.audioContext.current.createGain();
      
    // Create beat noise. First beat in bar has higher frequency
    osc.frequency.value = (beatNumber + 1) % this.state.beatsPerBar === 0 ? 1000 : 800;
    envelope.gain.value = 1;
    
    envelope.gain.exponentialRampToValueAtTime(1, time + 0.001);
    envelope.gain.exponentialRampToValueAtTime(0.001, time + 0.02);

    osc.connect(envelope);
    envelope.connect(this.audioContext.current.destination);

    osc.start(time);
    osc.stop(time + 0.03);
  }

  /**
   * Called by the timer.
   * Schedules next beat when needed (as opposed to infinitely).
   */
  scheduler = () => {
    if(this.state.beatsPerBar === (this.state.currentBeatInBar+1) && this.state.nextNoteTime < this.audioContext.current.currentTime + this.state.scheduleAheadTime){
      this.setState({
        lastbeat: true
      });
    }
    if (this.state.nextNoteTime < this.audioContext.current.currentTime + this.state.scheduleAheadTime) {
      this.scheduleBeat(this.state.currentBeatInBar, this.state.nextNoteTime);
      this.nextBeat();
      this.setState({
        isBeat: true
      });
    }
    else{
      this.setState({
        isBeat: false,
        lastbeat: false
      });
    }
  }

  /**
   * Toggle metronome playing.
   */
  startStopMetro = () => {
    if (!this.audioContext.current) {
      this.audioContext.current = new AudioContext();
    }
    if (this.state.isPlaying === false) {
      this.setState({
        nextNoteTime: this.audioContext.current.currentTime + 0.05,
        timerID: setInterval(this.scheduler, this.state.lookahead),
      });
    } else {
      clearInterval(this.state.timerID);
    }
    
    this.setState(state => ({isPlaying: !state.isPlaying}));
  }

  /**
   * Decrease BPM.
   */
  decBPM = () => {
    // Prevent 0 tempo
    this.setState({
      bpm: this.state.bpm - 10 === 0
        ? this.state.bpm
        : this.state.bpm - 10
    });
  }

  /**
   * Increase BPM.
   */
  incBPM = () => {
    // Max tempo is 240
    this.setState({
      bpm: this.state.bpm + 10 > 240 
        ? this.state.bpm
        : this.state.bpm + 10
    });
  }

  componentWillUnmount() {
    clearInterval(this.state.timerID);
  }

  render() {
    let theme = this.context[0];
    return ( 
      <div className="metronome">
        <Flex flexDir="column">
          <Flex flexDir="row" alignItems="center">
            <Box>
              <div className={this.state.isPlaying ? "btn metro playing" : "btn metro"} onClick={this.startStopMetro}>
                <img
                  src={theme === "light" ? image_metronome : image_metronome_white}
                  alt="Start/Stop Metronome" height={50} width={50}/>
              </div>
            </Box>
            <Flex flexDir="column" alignItems="center">
              <Box>
                <div className="metro bpm">
                  {this.state.bpm}
                </div>
              </Box>
              <Box width={80}>
                <div className="btn bpm" onClick={this.decBPM}>
                  -
                </div>
                <div className="btn bpm" onClick={this.incBPM}>
                  +
                </div>
              </Box>
            </Flex>
          </Flex>
          <Box>
            <div className={this.state.currentBeatInBar === 0 ? "prog on" : "prog off"}>
              <div className='btn inv'/>
            </div>
            <div className={(this.state.currentBeatInBar === 1) ? "prog on" : "prog off"}>
              <div className='btn inv'/>
            </div>
            <div className={((this.state.currentBeatInBar === 2) && this.state.btn3 === true) ? "prog on" : "prog off"}>
              <div className={(this.state.btn3 === true) ? "btn cb" : "btn cb off"} onClick={this.chgbtn3}/>
            </div>
            <div className={((this.state.currentBeatInBar === 3 ) && this.state.btn4 === true) ? "prog on" : "prog off"}>
              <div className={(this.state.btn4 === true) ? "btn cb" : "btn cb off"} onClick={this.chgbtn4}/>
            </div>
            <div className={((this.state.currentBeatInBar === 4 ) && this.state.btn5 === true) ? "prog on" : "prog off"}>
              <div className={(this.state.btn5 === true) ? "btn cb" : "btn cb off"} onClick={this.chgbtn5}/>
            </div>
            <div className={((this.state.currentBeatInBar === 5 ) && this.state.btn6 === true) ? "prog on" : "prog off"}>
              <div className={(this.state.btn6 === true) ? "btn cb" : "btn cb off"} onClick={this.chgbtn6}/>
            </div>
          </Box>
        </Flex>
      </div>
    );
  }
}
Metronome.contextType = ThemeContext;

export default Metronome;