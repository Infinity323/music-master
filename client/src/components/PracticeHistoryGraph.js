import { useContext, useEffect, useState } from 'react';
import { Chart, CategoryScale, LinearScale, PointElement, LineElement, TimeScale, Title, Tooltip, Legend } from 'chart.js';
import 'chartjs-adapter-date-fns';
import { format } from 'date-fns';
import annotationPlugin from 'chartjs-plugin-annotation';
import { Line } from 'react-chartjs-2'
import { useNavigate } from 'react-router-dom';
import Modal from 'react-modal'
import { Box, Flex } from '@chakra-ui/react';
import { baseUrl, style } from '../App';
import loading_gif from '../assets/images/loading_gif.gif'
import { SheetMusicIdContext } from '../utils/Contexts';
import PracticeHistoryGraphOptions from './PracticeHistoryOptions';

Chart.register(CategoryScale, LinearScale, PointElement, LineElement, TimeScale, Title, Tooltip, Legend, annotationPlugin);
Chart.defaults.font.family = "AppleRegular";

function PracticeHistoryGraph() {
  const textColor = style.getPropertyValue('--text-color');
  
  const navigate = useNavigate();
  // Module rendering hooks
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  // Chart data rendering hooks
  const selectedMusic = useContext(SheetMusicIdContext)[0];
  const [performances, setPerformances] = useState([]);
  const [goals, setGoals] = useState([]);
  const [data, setData] = useState({});
  const [showGoals, setShowGoals] = useState(true);
  const [timeWindow, setTimeWindow] = useState("all");
  const [timeWindowOffset, setTimeWindowOffset] = useState(Number.MAX_SAFE_INTEGER);
  // Chart interactivity hooks
  const [selectedGoal, setSelectedGoal] = useState(-1);

  // Line chart options
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
      annotation: {
        // Goals render as chart annotations
        annotations: [
          // TODAY line
          {
            type: 'line',
            xMin: new Date(),
            xMax: new Date(),
            yMin: 0,
            yMax: 100,
            borderColor: 'red',
            borderWidth: 2,
            label: {
              content: "TODAY",
              position: 'end',
              display: true
            },
            display: showGoals
          }
        ].concat(goals.flatMap(item => item.sheet_music_id === selectedMusic &&
          Date.now().valueOf() - new Date(item.end_date).valueOf() <= timeWindowOffset
          ?
            {
              type: 'line',
              xMin: new Date(item.end_date),
              xMax: new Date(item.end_date),
              yMin: 0,
              yMax: 100,
              value: item.id,
              borderColor: 'rgb(98, 232, 31)',
              borderWidth: 2,
              label: {
                content: [
                  "Goal: " + item.name,
                  format(new Date(item.end_date), 'M/dd/yy'),
                  "Tuning: " + item.tuning_percent_accuracy * 100,
                  "Tempo: " + item.tempo_percent_accuracy * 100,
                  "Dynamics: " + item.dynamics_percent_accuracy * 100
                ],
                position: 'end',
                display: false
              },
              display: showGoals,
              click({element}) {
                setSelectedGoal(element.options.value);
                element.label.options.display = true;
                element.options.borderWidth = 5;
                return true;
              },
              enter({element}) {
                element.label.options.display = true;
                element.options.borderWidth = 5;
                return true;
              },
              leave({element}) {
                if (element.options.value !== selectedGoal) {
                  element.label.options.display = false;
                  element.options.borderWidth = 2;
                }
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
            millisecond: "M/dd/yy H:mm:ss",
            second: "M/dd/yy H:mm:ss",
            minute: "M/dd/yy H:mm",
            hour: "M/dd/yy H:mm",
            day: "M/dd/yy",
            week: "M/dd/yy",
            month: "M/dd/yy",
          }
        }
      }
    },
    parsing: {
      xAxisKey: 'time',
      yAxisKey: 'value'
    }
  };

  // Time window offsets (ms)
  const timeWindowOffsets = [
    { type: "day", value: 86400000 },
    { type: "three-days", value: 259200000 },
    { type: "week", value: 604800000 },
    { type: "month", value: 2678400000 },
    { type: "all", value: Number.MAX_SAFE_INTEGER }
  ]

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
    setSelectedGoal(-1);
    setData({
      datasets: [
        // Actual performance metrics
        {
          label: 'Tuning',
          data: performances.flatMap(item => item.sheet_music_id === selectedMusic &&
            Date.now().valueOf() - new Date(item.date_time).valueOf() <= timeWindowOffset
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
          data: performances.flatMap(item => item.sheet_music_id === selectedMusic &&
            Date.now().valueOf() - new Date(item.date_time).valueOf() <= timeWindowOffset
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
          data: performances.flatMap(item => item.sheet_music_id === selectedMusic &&
            Date.now().valueOf() - new Date(item.date_time).valueOf() <= timeWindowOffset
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
  }, [selectedMusic, performances, goals, timeWindow]);
  useEffect(() => {
    setIsLoaded(true);
  }, [data]);
  
  function AddGoalButton() {
    const [modalIsOpen, setModalIsOpen] = useState(false);
    const [name, setName] = useState("");
    const [endDate, setEndDate] = useState("");
    const [tempoAccuracy, setTempoAccuracy] = useState("");
    const [averageTempo, setAverageTempo] = useState("");
    const [tuningAccuracy, setTuningAccuracy] = useState("");
    const [dynamicsAccuracy, setDynamicsAccuracy] = useState("");

    function openModal() {
      setModalIsOpen(true);
    }
    function closeModal() {
      setModalIsOpen(false);
    }

    function postGoal() {
      fetch(baseUrl + "/goal", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          "sheet_music_id": selectedMusic,
          "name": name,
          "start_date": "now()",
          "end_date": endDate,
          "tempo_percent_accuracy": tempoAccuracy ? tempoAccuracy : 0,
          "average_tempo": averageTempo ? averageTempo : 0,
          "tuning_percent_accuracy": tuningAccuracy ? tuningAccuracy : 0,
          "dynamics_percent_accuracy": dynamicsAccuracy ? dynamicsAccuracy : 0
        })
      }).then((res) => res.json())
        .then((data) => setGoals(goals.concat(data)));
      closeModal();
    }

    return (
      <>
        <div className={selectedMusic !== -1 ? "btn small" : "btn small disabled"} onClick={openModal}>
          Add Goal
        </div>
        <Modal isOpen={modalIsOpen} onRequestClose={closeModal} className="modal" overlayClassName="modal-overlay">
          <Flex flexDir={"row"}>
            <Box width={360}>
              Name
              <br/><input type="text" onChange={(e) => setName(e.target.value)}/><br/>
              {/* TODO: add better date selection */}
              Deadline (YYYY-MM-DD)
              <br/><input type="text" onChange={(e) => setEndDate(e.target.value)}/><br/>
            </Box>
            <Box width={360}>
              Average Tempo (e.g. "120")
              <br/><input type="text" onChange={(e) => setAverageTempo(e.target.value)}/><br/>
              Tempo % Accuracy (e.g. "100")
              <br/><input type="text" onChange={(e) => setTempoAccuracy(e.target.value / 100)}/><br/>
              Tuning % Accuracy (e.g. "100")
              <br/><input type="text" onChange={(e) => setTuningAccuracy(e.target.value / 100)}/><br/>
              Dynamics % Accuracy (e.g. "100")
              <br/><input type="text" onChange={(e) => setDynamicsAccuracy(e.target.value / 100)}/><br/>
              <br/>
            </Box>
          <div className="btn medium" id="submitForm" onClick={postGoal}>
            Submit
          </div>
          <div className="btn medium" id="closeForm" onClick={closeModal}>
            Cancel
          </div>
          </Flex>
        </Modal>
      </>
    );
  }

  function DeleteButton() {
    function deleteGoal() {
      fetch(baseUrl + "/goal/" + selectedGoal, {
        method: "DELETE"
      }).then((res) => res.json());
      const index = goals.findIndex(item => item.id === selectedGoal);
      goals.splice(index, 1);
      setGoals(goals);
      setSelectedGoal(-1);
    }

    return (
      <>
        <div className={selectedGoal === -1 ? "btn small disabled" : "btn small"} onClick={deleteGoal}>
          Delete Goal
        </div>
      </>
    );
  }

  function toggleGoals() {
    setShowGoals(!showGoals);
  }

  function changeTimeWindow(timeWindow) {
    setTimeWindow(timeWindow);
    setTimeWindowOffset(timeWindowOffsets.find(e => { return e.type === timeWindow; }).value)
  }

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
        <PracticeHistoryGraphOptions
          showGoals={showGoals}
          toggleGoals={toggleGoals}
          timeWindow={timeWindow}
          changeTimeWindow={changeTimeWindow}
        />
        <AddGoalButton/>
        <DeleteButton/>
      </>
    );
  }
}

export default PracticeHistoryGraph;