import { Chart, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import { Line } from "react-chartjs-2"

Chart.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);
Chart.defaults.font.family = "Segoe UI";

const { style } = document.documentElement;

function PracticeHistoryGraph() {
  const textColor = style.getPropertyValue('--text-color');

  const options = {
    responsive: true,
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

  const labels = ['2/10/23', '2/11/23', '2/12/23', '2/13/23', '2/14/23'];

  const data = {
    labels: labels,
    datasets: [
      {
        label: 'Pitch',
        data: [50, 60, 10, 20, 80],
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
      },
      {
        label: 'Tempo',
        data: [10, 20, 30, 40, 50],
        borderColor: 'rgb(53, 162, 235)',
        backgroundColor: 'rgba(53, 162, 235, 0.5)',
      },
      {
        label: 'Dynamics',
        data: [100, 90, 80, 70, 60],
        borderColor: 'rgb(191, 85, 236)',
        backgroundColor: 'rgba(191, 85, 236, 0.5)',
      }
    ],
  };

  return (
    <Line options={options} data={data}/>
  );
}

export default PracticeHistoryGraph;