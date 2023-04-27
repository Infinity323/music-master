import React, { Component } from 'react';
import { Chart, LinearScale, LogarithmicScale, PointElement, LineElement, Tooltip, Legend } from 'chart.js';
import { Scatter } from 'react-chartjs-2';
import annotationPlugin from 'chartjs-plugin-annotation';
import zoomPlugin from 'chartjs-plugin-zoom';
import { baseUrl, style } from '../App';
import { getNote, getNoteName, getOctave } from '../utils/AudioAnalyzer';

Chart.register(LinearScale, LogarithmicScale, PointElement, LineElement, Tooltip, Legend, annotationPlugin, zoomPlugin);
Chart.defaults.font.family = "AppleRegular";

const range = (from, to, step) =>
  [...Array(Math.floor((to - from) / step) + 1)].map((_, i) => from + i * step);

const FREQUENCY_TICKS = range(-24, 36, 1).map(x => 440.0*Math.pow(2, x/12)); // C2 to C7

const zoomOptions = {
  zoom: {
    pinch: { enabled: true },
    mode: 'x'
  },
  pan: {
    enabled: true,
    mode: 'x',
  },
  limits: {
    x: { min: 'original', max: 'original' }
  }
};

class PerformanceGraph extends Component {
  constructor(props) {
    super(props);
    this.performance = props.performance;
    this.state = {
      viewPitch: true,
      ideal: null,
      actual: null,
      pitchOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          zoom: zoomOptions
        }
      },
      pitchData: {
        datasets: []
      },
      dynamicsOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          zoom: zoomOptions
        }
      },
      dynamicsData: {
        datasets: []
      },
      measureTimes: null
    };

    this.textColor = style.getPropertyValue('--text-color');
    this.hoverColor = style.getPropertyValue('--hover-color');
    this.lineColor = style.getPropertyValue('--select-color');

    this.loadGraph = this.loadGraph.bind(this);
    this.loadMeasureAnnotations = this.loadMeasureAnnotations.bind(this);
    this.toggleView = this.toggleView.bind(this);
  }

  loadGraph() {
    this.setState({
      pitchData: {
        labels: this.state.measureNumbers,
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
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: false,
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
          },
          annotation: {
            annotations: this.state.measureTimes.map((x, index) => {
              return {
                type: 'line',
                xMin: x,
                xMax: x,
                borderColor: this.hoverColor,
                borderDash: [5, 15],
                borderWidth: 2,
                label: {
                  content: `${index + 1}`,
                  position: 'start',
                  display: true
                },
              };
            })
          },
          zoom: zoomOptions
        },
        scales: {
          x: {
            title: {
              display: true,
              text: 'Measure Numbers',
              color: this.textColor
            },
            ticks: {
              display: false
            }
          },
          y: {
            title: {
              display: true,
              text: 'Pitch',
              color: this.textColor
            },
            ticks: {
              callback: x => {
                let noteName = getNoteName(getNote(x));
                let octave = getOctave(getNote(x));
                let pitch = `${noteName}${octave}`;
                return pitch;
              }
            },
            afterBuildTicks: axis => axis.ticks = FREQUENCY_TICKS.map(v => ({ value: v })),
            type: 'logarithmic'
          }
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
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: false,
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
          },
          annotation: {
            annotations: this.state.measureTimes.map((x, index) => {
              return {
                type: 'line',
                xMin: x,
                xMax: x,
                borderColor: this.hoverColor,
                borderDash: [5, 15],
                borderWidth: 2,
                label: {
                  content: `${index + 1}`,
                  position: 'start',
                  display: true
                },
              };
            })
          },
          zoom: zoomOptions
        },
        scales: {
          x: {
            title: {
              display: true,
              text: 'Measure Numbers',
              color: this.textColor
            },
            ticks: {
              display: false
            }
          },
          y: {
            title: {
              display: true,
              text: 'Volume',
              color: this.textColor
            },
            ticks: {
              stepSize: 16
            },
            min: 0,
            max: 127
          }
        }
      }
    });
  }

  loadMeasureAnnotations() {
    let idealBpm = this.state.ideal.tempo;
    let actualBpm = this.performance.average_tempo;
    // Time scale ideal beats based on bpm difference
    let measureTimes = this.state.ideal.downbeat_locations.map(
      x => x * idealBpm / actualBpm
    );
    this.setState({
      measureTimes: measureTimes
    });
    this.setState(state => {
      let newIdeal = state.ideal;
      newIdeal.notes = newIdeal.notes.map(note => {
        return {
          pitch: note.pitch,
          velocity: note.velocity,
          start: note.start * idealBpm / actualBpm,
          end: note.end * idealBpm / actualBpm
        };
      });
      return {
        ideal: newIdeal
      };
    });
  }

  componentDidMount() {
    // Get performance details
    fetch(baseUrl + "/performance/" + this.performance.id + "/diff")
      .then(res => res.json())
      .then(result => this.setState({
        ideal: result.expected,
        actual: result.actual
      }))
      .catch(error => console.error(error));
  }

  componentDidUpdate(prevProps, prevState) {
    if (!prevState.ideal && this.state.ideal) {
      this.loadMeasureAnnotations();
    }
    if (prevState.measureTimes !== this.state.measureTimes) {
      this.loadGraph();
    }
  }

  toggleView() {
    this.setState(state => {
      return {viewPitch: !state.viewPitch}
    });
  }

  render() {
    return (
      <>
        <div className="chart performance">
          { this.state.viewPitch
            ? <Scatter options={this.state.pitchOptions} data={this.state.pitchData}/>
            : <Scatter options={this.state.dynamicsOptions} data={this.state.dynamicsData}/>
          }
        </div>
        <div className="btn small" onClick={this.toggleView}>
          Toggle View
        </div>
      </>
    );
  }
}
    
export default PerformanceGraph;