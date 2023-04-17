import React, { Component } from 'react';
import { Chart, LinearScale, LogarithmicScale, PointElement, LineElement, TimeScale, Title, Tooltip, Legend } from 'chart.js';
import { Scatter } from 'react-chartjs-2';
import { baseUrl, style } from '../App';
import { getNote, getNoteName, getOctave } from '../utils/AudioAnalyzer';

Chart.register(LinearScale, LogarithmicScale, PointElement, LineElement, Tooltip, Legend);
Chart.defaults.font.family = "AppleRegular";

class PerformanceGraph extends Component {
  constructor(props) {
    super(props);
    this.performanceId = props.performanceId;
    this.state = {
      viewPitch: true,
      measures: [],
      ideal: [],
      actual: [],
      pitchOptions: {},
      pitchData: {
        datasets: []
      },
      dynamicsOptions: {},
      dynamicsData: {
        datasets: []
      }
    };

    this.textColor = style.getPropertyValue('--text-color');
    this.lineColor = style.getPropertyValue('--select-color');

    this.loadGraph = this.loadGraph.bind(this);
    this.toggleView = this.toggleView.bind(this);
  }

  loadGraph() {
    this.setState({
      pitchData: {
        datasets: [
          {
            label: "Actual Pitch",
            data: this.state.actual.notes.map(item => {
              return {
                x: item.start,
                y: item.pitch
              }
            }),
            backgroundColor: this.lineColor,
            borderColor: this.lineColor,
            showLine: true,
            stepped: true,
          },
          {
            label: "Ideal Pitch",
            data: this.state.ideal.notes.map(item => {
              return {
                x: item.start,
                y: item.pitch
              }
            }),
            backgroundColor: '#B2BABB',
            borderColor: '#B2BABB',
            showLine: true,
            stepped: true,
          }
        ]
      },
      pitchOptions: {
        plugins: {
          title: {
            display: true,
            text: 'Notes Detected',
            color: this.textColor
          },
          tooltip: {
            callbacks: {
              label: (context, elements) => {
                let label = context.dataset.label;
                let notes = label === "Actual Pitch"
                  ? this.state.actual.notes : this.state.ideal.notes;
                let i = context.dataIndex;
                let freq = notes[i].pitch;
                let noteName = getNoteName(getNote(freq));
                let octave = getOctave(getNote(freq));
                return [
                  `Pitch: ${noteName}${octave} (${freq.toFixed(2)} Hz)`,
                  `Volume: ${notes[i].velocity}`,
                  `(From t=${notes[i].start.toFixed(2)} to t=${notes[i].end.toFixed(2)})`,
                ];
              }
            }
          }
        },
        responsive: true,
        scales: {
          x: {
            title: {
              display: true,
              text: 'Time (s)',
              color: this.textColor
            }
          },
          y: {
            title: {
              display: true,
              text: 'Pitch (Hz)',
              color: this.textColor
            },
            type: 'logarithmic'
          },
        }
      },
      dynamicsData: {
        datasets: [
          {
            label: "Actual Volume",
            data: this.state.actual.notes.map(item => {
              return {
                x: item.start,
                y: item.velocity
              }
            }),
            backgroundColor: this.lineColor,
            borderColor: this.lineColor,
            showLine: true,
            stepped: true,
          },
          {
            label: "Ideal Volume",
            data: this.state.ideal.notes.map(item => {
              return {
                x: item.start,
                y: item.velocity
              };
            }),
            backgroundColor: '#B2BABB',
            borderColor: '#B2BABB',
            showLine: true,
            stepped: true,
          }
        ]
      },
      dynamicsOptions: {
        plugins: {
          title: {
            display: true,
            text: 'Volume Level',
            color: this.textColor
          },
          tooltip: {
            callbacks: {
              label: (context, elements) => {
                let label = context.dataset.label;
                let notes = label === "Actual Volume"
                  ? this.state.actual.notes : this.state.ideal.notes;
                let i = context.dataIndex;
                let freq = notes[i].pitch;
                let noteName = getNoteName(getNote(freq));
                let octave = getOctave(getNote(freq));
                return [
                  `Pitch: ${noteName}${octave} (${freq.toFixed(2)} Hz)`,
                  `Volume: ${notes[i].velocity}`,
                  `(From t=${notes[i].start.toFixed(2)} to t=${notes[i].end.toFixed(2)})`,
                ];
              }
            }
          }
        },
        responsive: true,
        scales: {
          x: {
            title: {
              display: true,
              text: 'Time (s)',
              color: this.textColor
            }
          },
          y: {
            title: {
              display: true,
              text: 'Volume',
              color: this.textColor
            },
            min: 0,
            max: 127
          },
        }
      }
    });
  }

  componentDidMount() {
    fetch(baseUrl + "/performance/" + this.performanceId + "/diff")
      .then(res => res.json())
      .then(result => this.setState({
        ideal: result.expected,
        actual: result.actual
      }))
      .then(this.loadGraph)
      .catch(error => console.error(error));
  }

  toggleView() {
    this.setState(state => {
      return {viewPitch: !state.viewPitch}
    });
  }

  render() {
    return (
      <div>
        { this.state.viewPitch
          ? <Scatter options={this.state.pitchOptions} data={this.state.pitchData}/>
          : <Scatter options={this.state.dynamicsOptions} data={this.state.dynamicsData}/>
        }
        <div className="btn small" onClick={this.toggleView}>
          Toggle View
        </div>
      </div>
    );
  }
}
    
export default PerformanceGraph;