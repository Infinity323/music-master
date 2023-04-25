import React, { Component } from 'react';
import image_metronome from '../assets/images/metronome.png';
import image_metronome_white from '../assets/images/metronome_white.png';
import { Flex, Box, Center, Checkbox } from '@chakra-ui/react';
import { ThemeContext } from '../utils/Contexts';
import { style } from '../App';

// Metronome built using this as guidance.
// https://grantjam.es/creating-a-simple-metronome-using-javascript-and-the-web-audio-api/
class MetronomeRecording extends Component {
  constructor(props) {
    super(props);

    this.audioContext = React.createRef();
    this.audioContext.current = null;
    
    this.state = {
      // User-customizable state variables
      currentBeatInBar: 0,
      beatsPerBar: 4,
      bpm: props.bpm,
      vol_f1: 1000,
      vol_f2: 800,
      vol_g: 1,
      // Internal state variables
      lookahead: 25,
      scheduleAheadTime: 0.1,
      nextNoteTime: 0.0,
      timerID: null,
      isPlaying: false,
      isBeat: false
    };
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
    osc.frequency.value = (beatNumber + 1) % this.state.beatsPerBar === 0 ? this.state.vol_f1 : this.state.vol_f2; //1000 800
    envelope.gain.value = this.state.vol_g; //1
    
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
  decBPB = () => {
    // Prevent 0 tempo
    this.setState({
      beatsPerBar: this.state.beatsPerBar - 1 === 1
        ? this.state.beatsPerBar
        : this.state.beatsPerBar - 1
    });
  }

  /**
   * Increase BPM.
   */
  incBPB = () => {
    // Max tempo is 240
    this.setState({
      beatsPerBar: this.state.beatsPerBar + 1 === 7
        ? this.state.beatsPerBar
        : this.state.beatsPerBar + 1
    });
  }

  componentWillUnmount() {
    clearInterval(this.state.timerID);
  }

  handleCheckboxChange = (event) => {
    if (event.target.checked) {
      this.setState({ 
        vol_f1: 1000,
        vol_f2: 800,
        vol_g: 1
      });
    } else {
      this.setState({ 
        vol_f1: 0,
        vol_f2: 0,
        vol_g: 0
      });
    }
  };

  render() {
    let theme = this.context[0];
    let textColor = style.getPropertyValue("--text-color");
    let btnColor = style.getPropertyValue("--btn-color");
    return ( 
      <div
        className={
          this.state.isPlaying
          ? this.state.currentBeatInBar === 0
            ? "metronome-rec beat downbeat"
            : this.state.currentBeatInBar % 2 === 0
              ? "metronome-rec beat even"
              : "metronome-rec beat odd"
          : "metronome-rec"
        }
      >
        <Flex flexDir="column" justifyContent="center" alignItems="center" height="100%">
          <Checkbox
            iconColor={textColor}
            iconSize="1rem"
            defaultChecked
            backgroundColor={btnColor}
            margin="5px"
            padding="2px"
            borderRadius="5px"
            boxShadow={"0px 0px 2px rgba(1, 1, 1, 0.2)"}
            onChange={this.handleCheckboxChange}
          >
            Sound
          </Checkbox>
          <Box>
            <div
              className={this.state.isPlaying ? "btn metro-rec on" : "btn metro-rec"}
              onClick={this.startStopMetro}
            >
              <img
                className="metro-rec"
                src={theme === "light" ? image_metronome : image_metronome_white}
                alt="Start/Stop Metronome"
              />
            </div>
          </Box>
          <Flex flexDir="row" alignItems="center">
            <div className="btn bpm" onClick={this.decBPB}>
              -
            </div>
            <div className="metro bpm">
              {this.state.beatsPerBar}
            </div>
            <div className="btn bpm" onClick={this.incBPB}>
              +
            </div>
          </Flex>
        </Flex>
      </div>
    );
  }
}
MetronomeRecording.contextType = ThemeContext;

export default MetronomeRecording;