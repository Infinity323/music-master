import React, { Component } from 'react';
import Chart from 'chart.js/auto';

class PerformanceGraph extends Component {
  constructor(props) {
    super(props);
    this.chartRef = React.createRef();
    this.chart = null;
    this.state = {
      data: {
        measures: [
          {
            "ideal_idx": 1, /* index number in musicXML array */
            "ideal_val": { /* note object in musicXML array */
                "pitch": 293.66, /* frequency */
                "velocity": 80, /* 0-127 MIDI velocity */
                "start": 1.3, /* start time of note in seconds */
                "end": 2 /* end time of note in seconds */
            },
            "actual_idx": 1, /* index number in recording .wav array */
            "actual_val": { /* note object in .way array */
                "pitch": 440.0,
                "velocity": 80,
                "start": 1.3,
                "end": 2
            },
            "diff_type": "pitch", /* difference type (pitch, velocity, start, end, extra, and missing) */
            "note_info": { /* note info object */
                "element": "note", /* can be note or rest */
                "name": "B-3", /* the name of the note */
                "type": "quarter", /* the type of note */
                "measure": 1, /* measure number */
                 "position": 1 /* position of the note in the measure */
            }
        },
        {
            "ideal_idx": 2, /* index number in musicXML array */
            "ideal_val": { /* note object in musicXML array */
                "pitch": 273.66, /* frequency */
                "velocity": 80, /* 0-127 MIDI velocity */
                "start": 3.0, /* start time of note in seconds */
                "end": 4 /* end time of note in seconds */
            },
            "actual_idx": 1, /* index number in recording .wav array */
            "actual_val": { /* note object in .way array */
                "pitch": 340.0,
                "velocity": 80,
                "start": 3.0,
                "end": 4
            },
            "diff_type": "pitch", /* difference type (pitch, velocity, start, end, extra, and missing) */
            "note_info": { /* note info object */
                "element": "note", /* can be note or rest */
                "name": "B-3", /* the name of the note */
                "type": "quarter", /* the type of note */
                "measure": 2, /* measure number */
                 "position": 2 /* position of the note in the measure */
            }
        },
        {
          "ideal_idx": 2, /* index number in musicXML array */
          "ideal_val": { /* note object in musicXML array */
              "pitch": 213.66, /* frequency */
              "velocity": 80, /* 0-127 MIDI velocity */
              "start": 3.23, /* start time of note in seconds */
              "end": 3.5 /* end time of note in seconds */
          },
          "actual_idx": 1, /* index number in recording .wav array */
          "actual_val": { /* note object in .way array */
              "pitch": 370.0,
              "velocity": 80,
              "start": 3.23,
              "end": 3.5
          },
          "diff_type": "pitch", /* difference type (pitch, velocity, start, end, extra, and missing) */
          "note_info": { /* note info object */
              "element": "note", /* can be note or rest */
              "name": "B-3", /* the name of the note */
              "type": "quarter", /* the type of note */
              "measure": 2, /* measure number */
               "position": 2 /* position of the note in the measure */
          }
        },
        {
          "ideal_idx": 2, /* index number in musicXML array */
          "ideal_val": { /* note object in musicXML array */
              "pitch": 390.66, /* frequency */
              "velocity": 80, /* 0-127 MIDI velocity */
              "start": 5.1, /* start time of note in seconds */
              "end": 5.8 /* end time of note in seconds */
          },
          "actual_idx": 1, /* index number in recording .wav array */
          "actual_val": { /* note object in .way array */
              "pitch": 400.0,
              "velocity": 80,
              "start": 5.1,
              "end": 5.8
          },
          "diff_type": "pitch", /* difference type (pitch, velocity, start, end, extra, and missing) */
          "note_info": { /* note info object */
              "element": "note", /* can be note or rest */
              "name": "B-3", /* the name of the note */
              "type": "quarter", /* the type of note */
              "measure": 2, /* measure number */
               "position": 2 /* position of the note in the measure */
          }
      },
        {
            "ideal_idx": 3, /* index number in musicXML array */
            "ideal_val": { /* note object in musicXML array */
                "pitch": 333.66, /* frequency */
                "velocity": 80, /* 0-127 MIDI velocity */
                "start": 5.5, /* start time of note in seconds */
                "end": 6 /* end time of note in seconds */
            },
            "actual_idx": 3, /* index number in recording .wav array */
            "actual_val": { /* note object in .way array */
                "pitch": 320.0,
                "velocity": 80,
                "start": 5.5,
                "end": 6
            },
            "diff_type": "pitch", /* difference type (pitch, velocity, start, end, extra, and missing) */
            "note_info": { /* note info object */
                "element": "note", /* can be note or rest */
                "name": "B-3", /* the name of the note */
                "type": "quarter", /* the type of note */
                "measure": 3, /* measure number */
                 "position": 3 /* position of the note in the measure */
            }
        }
        ]
      }
    };
  }

  componentDidMount() {
    const { measures } = this.state.data;
    const starttime = measures.map(item => item.actual_val.start);
    const ideal = measures.map(item => (item.ideal_val.pitch));
    const actual = measures.map(item => (item.actual_val.pitch));
    const difference = measures.map(item => Math.abs(item.actual_val.pitch-item.ideal_val.pitch));
    const notenames = measures.map(item => (item.note_info.name));
    const measpos = measures.map(item => ("("+item.note_info.measure+", "+item.note_info.position+")"));

    if (this.chart) {
      this.chart.destroy();
    }

    this.chart = new Chart(this.chartRef.current, { 
      type: 'bar',
      data: {
        labels: measpos,
        datasets: [
          {
            label: "Ideal",
            data: ideal,
            backgroundColor: 'white',
            borderColor: 'white',
            fill: false
          },
          {
            label: "Difference",
            data: difference,
            backgroundColor: 'red',
            borderColor: 'red',
            fill: false
          },
          {
            label: "Actual",
            data: actual,
            backgroundColor: 'grey',
            borderColor: 'grey',
            fill: false
          }
        ]
      },
      options: {
        plugins: {
          title: {
            display: true,
            text: 'Ideal V. Actual Pitch',
          },
        },
        responsive: true,
        scales: {
          x: {
            title: {
              display: true,
              text: '(Measure, Position)',
            },
            stacked: true,
          },
          y: {
            title: {
              display: true,
              text: 'Pitch',
            },
            stacked: true,
          },
        },
        onClick: (e, elements, chart) => {
          if (elements[0])
            alert(notenames[elements[0].index])
            //console.log(notenames[elements[0].index]);
          // alert(this.chart.getElementById(e))
        }
      }
    });
  }
  

  render() {
    return (
      <div>
        <canvas ref={this.chartRef} />
      </div>
    );
  }
}
    
export default PerformanceGraph;