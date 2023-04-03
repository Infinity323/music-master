import React, { Component } from 'react'
import image_metronome from '../assets/images/metronome.png'
import { Flex, Box, CircularProgress, CircularProgressLabel } from '@chakra-ui/react';

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
      BPM: 100,
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
    if(this.state.currentBeatInBar === 4){
      this.setState(state => ({
        currentBeatInBar: (state.currentBeatInBar - 4)
      }));
    }
    else{
      this.setState(state => ({
        currentBeatInBar: (state.currentBeatInBar + 1)
      }));
    }
    var secondsPerBeat = 60.0 / this.state.BPM;
    this.setState(state => ({
      nextNoteTime: state.nextNoteTime + secondsPerBeat,
      //currentBeatInBar: (state.currentBeatInBar + 1) % state.beatsPerBar
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
    osc.frequency.value = beatNumber === 0 ? 1000 : 800;
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
    if (this.state.nextNoteTime < this.audioContext.current.currentTime + this.state.scheduleAheadTime) {
      this.scheduleBeat(this.state.currentBeatInBar, this.state.nextNoteTime);
      this.nextBeat();
      this.setState({
        isBeat: true
      });
    }
    else{
      this.setState({
        isBeat: false
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
      BPM: this.state.BPM - 10 === 0
        ? this.state.BPM
        : this.state.BPM - 10
    });
  }

  /**
   * Increase BPM.
   */
  incBPM = () => {
    // Max tempo is 240
    this.setState({
      BPM: this.state.BPM + 10 > 240 
        ? this.state.BPM
        : this.state.BPM + 10
    });
  }

  componentWillUnmount() {
    clearInterval(this.state.timerID);
  }

  render() {
    return ( 
      <div className={this.state.isBeat ? "metronome-playing" : "metronome"}>
        <Flex flexDir="row" alignItems="center">
          <Box>
            <div className="btn metro" onClick={this.startStopMetro}>
              <img src={image_metronome} id="metronome" alt="Start/Stop Metronome"/>
            </div>
          </Box>
          <Flex flexDir="column" alignItems="center">
            <Box>
              <div className="metro bpm">
                {this.state.BPM}
              </div>
            </Box>
            <Box>
              <CircularProgress value={this.state.currentBeatInBar > 0 ? 100 : 0} size='15px' color='green' thickness='18px'>
                <CircularProgressLabel>{1}</CircularProgressLabel>
              </CircularProgress>
              <CircularProgress value={this.state.currentBeatInBar > 1 ? 100 : 0} size='15px' color='green' thickness='18px'>
                <CircularProgressLabel>{2}</CircularProgressLabel>
              </CircularProgress>
              <CircularProgress value={this.state.currentBeatInBar > 2 ? 100 : 0} size='15px' color='green' thickness='18px'>
                <CircularProgressLabel>{3}</CircularProgressLabel>
              </CircularProgress>
              <CircularProgress value={this.state.currentBeatInBar > 3 ? 100 : 0} size='15px' color='green' thickness='18px'>
                <CircularProgressLabel>{4}</CircularProgressLabel>
              </CircularProgress>
            </Box>
            <Box>
              <div className="btn bpm" onClick={this.decBPM}>
                -
              </div>
              <div className="btn bpm" onClick={this.incBPM}>
                +
              </div>
            </Box>
          </Flex>
        </Flex>
      </div>
    );
  }
}

export default Metronome;