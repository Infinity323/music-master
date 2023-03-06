import React, { Component } from 'react'
import sound_metronome from "../assets/sounds/metronome.wav"
import image_metronome from "../assets/images/metronome.png"
import { Flex, Box } from '@chakra-ui/react';

export class MetronomeButton extends Component {
  constructor(props) {
    super(props);

    this.state = {
      BPM: 50,
      isPlaying: false
    };
  }

  play = () => {
    new Audio(sound_metronome).play();
  }

  startMetro = () => {
    // TODO: sometimes setInterval is laggy. consider using webaudio api in addition
    // https://grantjam.es/creating-a-simple-metronome-using-javascript-and-the-web-audio-api/
    if (this.state.isPlaying === false) {
      this.setState({isPlaying: true});
      //call play multiple times
      this.timer = setInterval(this.play, (60 / this.state.BPM) * 1000); //(function,milliseconds)
    }
    else {
      clearInterval(this.timer);
      this.setState({isPlaying: false});
    }
  }

  decBPM = () => {
    this.setState({BPM: this.state.BPM - 10});
    if (this.state.isPlaying) {
      clearInterval(this.timer);
      this.timer = setInterval(this.play, (60 / this.state.BPM) * 1000);
    }
  }

  incBPM = () => {
    this.setState({BPM: this.state.BPM + 10});
    if (this.state.isPlaying) {
      clearInterval(this.timer);
      this.timer = setInterval(this.play, (60 / this.state.BPM) * 1000);
    }
  }

  componentWillUnmount() {
    clearInterval(this.timer);
  }

  render() {
    return ( 
      <div className="metro">
        <Flex flexDir="row" alignItems="center">
          <Box>
            <div className="btn metro"
              onClick={this.startMetro}
              >
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
              <div className="btn bpm"
                onClick={this.decBPM}
                >
                -
              </div>
              <div className="btn bpm"
                onClick={this.incBPM}
                >
                +
              </div>
            </Box>
          </Flex>
        </Flex>
      </div>
    );
  }
}