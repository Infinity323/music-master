import { useContext, useEffect, useState } from 'react';
import { Chart, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import { Line } from 'react-chartjs-2'
import { baseUrl, SheetMusicIdContext } from '../App';
import loading_gif from '../assets/images/loading_gif.gif'
import { style } from '../App';
import { useNavigate } from 'react-router-dom';

Chart.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);
Chart.defaults.font.family = "Segoe UI";

function PracticeHistoryGraph() {
  const textColor = style.getPropertyValue('--text-color');

  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [items, setItems] = useState([]);
  const [labels, setLabels] = useState([]);
  const [data, setData] = useState({});
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
      }
    },
    scales: {
      y: {
        max: 100,
        min: 0,
        ticks: {
          color: textColor,
          font: {
            size: 13
          }
        }
      },
      x: {
        ticks: {
          color: textColor,
          font: {
            size: 13
          }
        }
      }
    },
    parsing: {
      xAxisKey: 'id',
      yAxisKey: 'value'
    }
  };

  // Sequential useEffect(). items -> selectedMusic -> labels -> data
  useEffect(() => {
    fetch(baseUrl + "/performance")
      .then(res => res.json())
      .then(
        (result) => {
          setIsLoaded(false);
          setItems(result);
        },
        (error) => {
          setIsLoaded(true);
          setError(error);
        }
      )
  }, []);
  useEffect(() => {
    setIsLoaded(false);
    const dateTimeOptions = { timeZone: "UTC", hour: "numeric", minute: "numeric" };
    setLabels(items.flatMap(item => item.sheet_music_id === selectedMusic ?
      new Date(Date.parse(item.date_time)).toLocaleDateString("en-US", dateTimeOptions) :
      []));
  }, [selectedMusic, items]);
  useEffect(() => {
    setIsLoaded(false);
    setData({
      labels: labels,
      datasets: [
        {
          label: 'Tuning',
          data: items.flatMap(item => item.sheet_music_id === selectedMusic ?
            {id: item.sheet_music_id, value: item.tuning_percent_accuracy * 100} : [{}]
          ),
          borderColor: 'rgb(255, 99, 132)',
          backgroundColor: 'rgba(255, 99, 132, 0.5)',
          spanGaps: true,
        },
        {
          label: 'Tempo',
          data: items.flatMap(item => item.sheet_music_id === selectedMusic ?
            {id: item.sheet_music_id, value: item.tempo_percent_accuracy * 100} : [{}]
          ),
          borderColor: 'rgb(53, 162, 235)',
          backgroundColor: 'rgba(53, 162, 235, 0.5)',
          spanGaps: true
        },
        {
          label: 'Dynamics',
          data: items.flatMap(item => item.sheet_music_id === selectedMusic ?
            {id: item.sheet_music_id, value: item.dynamics_percent_accuracy * 100} : [{}]
          ),
          borderColor: 'rgb(191, 85, 236)',
          backgroundColor: 'rgba(191, 85, 236, 0.5)',
          spanGaps: true
        }
      ],
    });
  }, [selectedMusic, items, labels]);
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
      <div className="chart">
        <Line options={options} data={data}/>
      </div>
    );
  }
}

export default PracticeHistoryGraph;