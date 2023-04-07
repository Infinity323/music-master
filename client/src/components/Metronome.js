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
      btn3: false,
      btn4: false,
      btn5: false,
      btn6: false,
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
    if(this.state.btn5 === false){
      this.setState(state => ({
        beatsPerBar: 4
      }));
    }
  }
  nextBeat = () => {
    if(this.state.currentBeatInBar >= 2 && this.state.btn3 === true && this.state.btn4 === false){
      this.setState(state => ({
        currentBeatInBar: 0
      }));
    }
    else if(this.state.currentBeatInBar >= 3 && this.state.btn4 === true && this.state.btn5 === false){
      this.setState(state => ({
        currentBeatInBar: 0
      }));
    }
    else if(this.state.currentBeatInBar >= 4 && this.state.btn5 === true && this.state.btn6 === false){
      this.setState(state => ({
        currentBeatInBar: 0
      }));
    }
    else if(this.state.currentBeatInBar >= 5 && this.state.btn5 === true && this.state.btn6 === true){
      this.setState(state => ({
        currentBeatInBar: 0
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
              <img src={image_metronome} alt="Start/Stop Metronome" height={50} width={50}/>
            </div>
          </Box>
          <Flex flexDir="column" alignItems="center">
            <Box>
              <div className="metro bpm">
                {this.state.BPM}
              </div>
            </Box>
            <Box>
              <CircularProgress value={this.state.currentBeatInBar >= 0 ? 100 : 0} size='22px' color='green' thickness='18px'>
                <CircularProgressLabel>{}</CircularProgressLabel>
              </CircularProgress>
              <CircularProgress value={this.state.currentBeatInBar >= 1 ? 100 : 0} size='22px' color='green' thickness='18px'>
                <CircularProgressLabel>{}</CircularProgressLabel>
              </CircularProgress>
              <CircularProgress value={(this.state.currentBeatInBar >= 2 && this.state.btn3 === true) ? 100 : 0} size='22px' color='green' thickness='18px'>
              <CircularProgressLabel><div className={(this.state.btn3 === true) ? "btn cb3" : "btn cb3off"} onClick={this.chgbtn3}></div></CircularProgressLabel>
              </CircularProgress>
              <CircularProgress value={(this.state.currentBeatInBar >= 3 && this.state.btn4 === true) ? 100 : 0} size='22px' color='green' thickness='18px'>
                <CircularProgressLabel><div className={(this.state.btn4 === true) ? "btn cb4" : "btn cb4off"} onClick={this.chgbtn4}></div></CircularProgressLabel>
              </CircularProgress>
              <CircularProgress value={(this.state.currentBeatInBar >= 4 && this.state.btn5 === true) ? 100 : 0} size='22px' color='green' thickness='18px'>
                <CircularProgressLabel><div className={(this.state.btn5 === true) ? "btn cb5" : "btn cb5off"} onClick={this.chgbtn5}></div></CircularProgressLabel>
              </CircularProgress>
              <CircularProgress value={((this.state.currentBeatInBar >= 5 && this.state.btn6 === true) ? 100 : 0)} size='22px' color='green' thickness='18px'>
                <CircularProgressLabel><div className={(this.state.btn6 === true) ? "btn cb6" : "btn cb6off"} onClick={this.chgbtn6}></div></CircularProgressLabel>
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