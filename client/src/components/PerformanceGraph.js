import React, { Component } from 'react';
import { Chart, CategoryScale, LinearScale, PointElement, LineElement, TimeScale, Title, Tooltip, Legend } from 'chart.js';
import { Line } from 'react-chartjs-2';
import { baseUrl } from '../App';

Chart.register(CategoryScale, LinearScale, PointElement, LineElement, TimeScale, Title, Tooltip, Legend);
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
      difference: [],
      notenames: [],
      notetypes: [],
      measpos: [],
      idealdyn: [],
      actualdyn: [],
      differencedyn: [],
      starttime: [],
      endtime: [],
      duration: [],
      pitchOptions: {},
      pitchData: {
        datasets: []
      },
      dynamicsOptions: {},
      dynamicsData: {
        datasets: []
      }
    };

    this.loadGraph = this.loadGraph.bind(this);
    this.toggleView = this.toggleView.bind(this);
  }

  loadGraph() {
    this.setState({
      pitchData: {
        labels: this.state.measpos,
        datasets: [
          {
            label: "Ideal Pitch",
            data: this.state.ideal,
            backgroundColor: 'white',
            borderColor: 'white',
            hidden: false,
            stepped: true,
          },
          {
            label: "Actual Pitch",
            data: this.state.actual,
            backgroundColor: 'black',
            borderColor: 'black',
            hidden: false,
            stepped: true,
          },
          {
            label: "Ideal Dynamics",
            data: this.state.idealdyn,
            backgroundColor: 'grey',
            borderColor: 'grey',
            hidden: true,
            stepped: true,
          },
          {
            label: "Actual Dynamics",
            data: this.state.actualdyn,
            backgroundColor: 'dark grey',
            borderColor: 'dark grey',
            hidden: true,
            stepped: true,
          }
        ]
      },
      pitchOptions: {
        plugins: {
          title: {
            display: true,
            text: 'Ideal V. Actual Pitch',
          },
          tooltip: {
            callbacks: {
              label: (context, elements) => {
                console.log(context);
                console.log(elements);
                return [
                  `${this.state.notenames[context.dataIndex]} - ${this.state.notetypes[context.dataIndex]}`,
                  `Played for ${this.state.duration[context.dataIndex]} seconds`,
                  `(From t=${this.state.starttime[context.dataIndex].toFixed(2)} to t=${this.state.endtime[context.dataIndex].toFixed(2)})`,
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
              text: '(Measure, Position)',
            }
          },
          y: {
            title: {
              display: true,
              text: 'Pitch',
            }
          },
        }
      }
    });
  }

  componentDidMount() {
    fetch(baseUrl + "/performance/" + this.performanceId + "/diff")
      .then(res => res.json())
      .then(result => this.setState({
        measures: result,
        ideal: result.map(item => (item.diff.ideal_val.pitch)),
        actual: result.map(item => (item.diff.actual_val.pitch)),
        difference: result.map(item => Math.abs(item.diff.actual_val.pitch-item.diff.ideal_val.pitch)),
        notenames: result.map(item => (item.note_info.name)),
        notetypes: result.map(item => (item.note_info.type)),
        measpos: result.map(item => ("("+item.note_info.measure+", "+item.note_info.position+")")),
        idealdyn: result.map(item => (item.diff.ideal_val.velocity)),
        actualdyn: result.map(item => (item.diff.actual_val.velocity)),
        differencedyn: result.map(item => Math.abs(item.diff.actual_val.velocity-item.diff.ideal_val.velocity)),
        starttime: result.map(item => item.diff.actual_val.start),
        endtime: result.map(item => item.diff.actual_val.end),
        duration: result.map(item => (item.diff.ideal_val.end-item.diff.ideal_val.start))
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
          ? <Line options={this.state.pitchOptions} data={this.state.pitchData}/>
          : <Line options={this.state.dynamicsOptions} data={this.state.dynamicsData}/>
        }
        <div className="btn small" onClick={this.toggleView}>
          Toggle View
        </div>
      </div>
    );
  }
}
    
export default PerformanceGraph;