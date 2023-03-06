import { useContext, useEffect, useState } from 'react';
import { Chart, CategoryScale, LinearScale, PointElement, LineElement, TimeScale, Title, Tooltip, Legend, Annot, elements } from 'chart.js';
import 'chartjs-adapter-date-fns';
import { format } from 'date-fns';
import annotationPlugin from 'chartjs-plugin-annotation';
import { Line } from 'react-chartjs-2'
import { useNavigate } from 'react-router-dom';
import { baseUrl, SheetMusicIdContext, style } from '../App';
import loading_gif from '../assets/images/loading_gif.gif'

Chart.register(CategoryScale, LinearScale, PointElement, LineElement, TimeScale, Title, Tooltip, Legend, annotationPlugin);
Chart.defaults.font.family = "Segoe UI";

function PracticeHistoryGraph() {
  const textColor = style.getPropertyValue('--text-color');

  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [performances, setPerformances] = useState([]);
  const [goals, setGoals] = useState([]);
  const [data, setData] = useState({});
  const [showGoals, setShowGoals] = useState(true);
  const selectedMusic = useContext(SheetMusicIdContext)[0];
  const navigate = useNavigate();

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    onClick: (e, elements, chart) => {
      if (elements[0]) {
        const i = elements[0].index;
        const performanceId = chart.data.datasets[0].data[i].id;
        navigate("/performance/" + performanceId);
      }
    },
    plugins: {
      legend: {
        labels: {
          color: textColor,
          font: {
            size: 14
          },
          filter: (item, chart) => {
            return !item.text.includes(' Goal');
          }
        },
        position: 'top',
      },
      title: {
        display: true,
        text: 'Practice History',
        color: textColor,
        font: {
          size: 20
        }
      },
      annotation: {
        annotations: [
          {
            type: 'line',
            xMin: new Date(),
            xMax: new Date(),
            yMin: 0,
            yMax: 100,
            borderColor: 'red',
            borderWidth: 1.5,
            label: {
              content: "TODAY",
              position: 'end',
              display: true
            },
            display: showGoals
          }
        ].concat(goals.flatMap(item => item.sheet_music_id === selectedMusic
          ?
            {
              type: 'line',
              xMin: new Date(item.end_date),
              xMax: new Date(item.end_date),
              yMin: 0,
              yMax: 100,
              borderColor: 'rgb(98, 232, 31)',
              borderWidth: 1.5,
              label: {
                content: [
                  "Goal " + format(new Date(item.end_date), 'M/dd/yy'),
                  "Tuning: " + item.tuning_percent_accuracy * 100,
                  "Tempo: " + item.tempo_percent_accuracy * 100,
                  "Dynamics: " + item.dynamics_percent_accuracy * 100
                ],
                position: 'end',
                display: false
              },
              display: showGoals,
              enter({element}) {
                element.label.options.display = true;
                return true;
              },
              leave({element}) {
                element.label.options.display = false;
                return true;
              }
            }
          : [{}]
          )
        ).filter(value => Object.keys(value).length !== 0)
      }
    },
    scales: {
      y: {
        min: 0,
        max: 100,
        ticks: {
          color: textColor,
          font: {
            size: 13
          }
        }
      },
      x: {
        type: 'time',
        time: {
          displayFormats: {
            second: "M/dd/yy HH:mm:ss",
            minute: "M/dd/yy HH:mm:ss",
            hour: "M/dd/yy HH:mm",
            day: "M/dd/yy",
            week: "M/dd/yy",
            month: "M/dd/yy",
          }
        },
        ticks: {
          source: 'data',
          color: textColor,
          font: {
            size: 13
          }
        }
      }
    },
    parsing: {
      xAxisKey: 'time',
      yAxisKey: 'value'
    }
  };

  useEffect(() => {
    // Grabs ALL performances and ALL goals from database on first render
    // Could change to only select performances and goals that match sheet_music_id
    fetch(baseUrl + "/performance")
      .then(res => res.json())
      .then(
        (result) => {
          setIsLoaded(false);
          setPerformances(result);
        },
        (error) => {
          setIsLoaded(true);
          setError(error);
        }
      );
    fetch(baseUrl + "/goal")
      .then(res => res.json())
      .then(
        (result) => {
          setIsLoaded(false);
          setGoals(result);
        },
        (error) => {
          setIsLoaded(true);
          setError(error);
        }
      );
  }, []);
  useEffect(() => {
    setIsLoaded(false);
    setData({
      datasets: [
        // Actual performance metrics
        {
          label: 'Tuning',
          data: performances.flatMap(item => item.sheet_music_id === selectedMusic
            ?
              {
                id: item.id,
                time: new Date(item.date_time),
                value: item.tuning_percent_accuracy * 100
              }
            : [{}]
          ),
          borderColor: 'rgb(243, 156, 18)',
          backgroundColor: 'rgba(243, 156, 18, 0.5)',
          spanGaps: true
        },
        {
          label: 'Tempo',
          data: performances.flatMap(item => item.sheet_music_id === selectedMusic
            ?
              {
                id: item.id,
                time: new Date(item.date_time),
                value: item.tempo_percent_accuracy * 100
              }
            : [{}]
          ),
          borderColor: 'rgb(53, 162, 235)',
          backgroundColor: 'rgba(53, 162, 235, 0.5)',
          spanGaps: true
        },
        {
          label: 'Dynamics',
          data: performances.flatMap(item => item.sheet_music_id === selectedMusic
            ?
              {
                id: item.id,
                time: new Date(item.date_time),
                value: item.dynamics_percent_accuracy * 100
              }
            : [{}]
          ),
          borderColor: 'rgb(191, 85, 236)',
          backgroundColor: 'rgba(191, 85, 236, 0.5)',
          spanGaps: true
        }
      ],
    });
  }, [selectedMusic, performances, goals, showGoals]);
  useEffect(() => {
    setIsLoaded(true);
  }, [data]);  
  
  if (error) {
    return (
      <div className="content">
        {error.name}: {error.message}
      </div>
    );
  } else if (!isLoaded) {
    return (
      <div className="content">
        <img src={loading_gif} width="30px" alt="Loading..."/>
      </div>
    );
  } else {
    return (
      <>
        <div className="chart">
          <Line options={options} data={data}/>
        </div>
        <div className="btn small" onClick={() => {setShowGoals(!showGoals)}}>
          Toggle Goals
        </div>
      </>
    );
  }
}

export default PracticeHistoryGraph;