import React, { Component } from 'react'
import sound_metronome from "../assets/sounds/metronome.wav"
import image_metronome from "../assets/images/metronome.png"
import { Flex, Box} from '@chakra-ui/react';

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

    startMetro =() =>{
      if(this.state.isPlaying === false){
        this.setState({isPlaying: true});
        //call play multiple times
        this.timer = setInterval(this.play, (60 / this.state.BPM) * 1000); //(function,milliseconds)
      }
      else{
        clearInterval(this.timer);
        this.setState({isPlaying: false});
      }

    };

    decBPM =() =>{
      this.setState({BPM: this.state.BPM - 10});
      if(this.state.isPlaying){
        clearInterval(this.timer);
        this.timer = setInterval(this.play, (60 / this.state.BPM) * 1000);
      }
    };

    incBPM =() =>{
      this.setState({BPM: this.state.BPM + 10});
      if(this.state.isPlaying){
        clearInterval(this.timer);
        this.timer = setInterval(this.play, (60 / this.state.BPM) * 1000);
      }
    };

  render(){
    return( 
      <div className="metro">
        <Flex flexDirection="column" alignItems="center" marginTop="-20px">
          <Box>
            <p>{this.state.BPM}</p>
          </Box>
          <Box marginTop="-30px">
            <button
              onClick={this.decBPM}
              >
              -
            </button>
            <button
              onClick={this.startMetro}
              >
              <img src = {image_metronome} height={10} width={20}/>
            </button>
            <button
              onClick={this.incBPM}
              >
              +
            </button>
          </Box>
        </Flex>
        
      </div>
    );
  }
}