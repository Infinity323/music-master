import { useEffect, useState } from 'react';
import { Chart, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import { Line } from 'react-chartjs-2'
import { baseUrl } from '../App';
import loading_gif from '../assets/images/loading_gif.gif'
import { style } from '../App';

Chart.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);
Chart.defaults.font.family = "Segoe UI";

function PracticeHistoryGraph({selectedMusic}) {
  const textColor = style.getPropertyValue('--text-color');

  const options = {
    responsive: true,
    maintainAspectRatio: false,
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
      },
    },
    scales: {
      y: {
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
    }
  };

  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [items, setItems] = useState([]);
  const [labels, setLabels] = useState([]);
  const [data, setData] = useState({});

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
      new Date(Date.parse(item.date_time), ).toLocaleDateString("en-US", dateTimeOptions) :
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
            item.tuning_percent_accuracy * 100 : []),
          borderColor: 'rgb(255, 99, 132)',
          backgroundColor: 'rgba(255, 99, 132, 0.5)',
          spanGaps: true
        },
        {
          label: 'Tempo',
          data: items.flatMap(item => item.sheet_music_id === selectedMusic ?
            item.tempo_percent_accuracy * 100 : []),
          borderColor: 'rgb(53, 162, 235)',
          backgroundColor: 'rgba(53, 162, 235, 0.5)',
          spanGaps: true
        },
        {
          label: 'Dynamics',
          data: items.flatMap(item => item.sheet_music_id === selectedMusic ?
            item.dynamics_percent_accuracy * 100 : []),
          borderColor: 'rgb(191, 85, 236)',
          backgroundColor: 'rgba(191, 85, 236, 0.5)',
          spanGaps: true
        }
      ],
    });
  }, [labels]);
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