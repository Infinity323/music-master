import { useContext, useState } from 'react';
import Modal from 'react-modal';
import ReactSlider from 'react-slider';
import { Box, Flex } from '@chakra-ui/react';
import { baseUrl } from '../App';
import { SheetMusicContext } from '../utils/Contexts';

function AddGoalButton({goals, setGoals}) {
  const selectedMusic = useContext(SheetMusicContext)[0].id;
  const [modalIsOpen, setModalIsOpen] = useState(false);
  // Goal data
  const [name, setName] = useState("");
  const [endDate, setEndDate] = useState(new Date().toJSON().slice(0, 10));
  const [averageTempo, setAverageTempo] = useState(120);
  const [tempoAccuracy, setTempoAccuracy] = useState(50);
  const [tuningAccuracy, setTuningAccuracy] = useState(50);
  const [dynamicsAccuracy, setDynamicsAccuracy] = useState(50);

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
        "tempo_percent_accuracy": tempoAccuracy/100,
        "average_tempo": averageTempo,
        "tuning_percent_accuracy": tuningAccuracy/100,
        "dynamics_percent_accuracy": dynamicsAccuracy/100
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
          <Box width={"50%"}>
            Name
            <br/>
            <input type="text" onChange={(e) => setName(e.target.value)} />
            <br/>
            <br/>
            <label for="goal">Deadline</label>
            <br/>
            <input type="date" id="goal" defaultValue={endDate} onChange={(e) => setEndDate(e.target.value)} />
            <br/>
          </Box>
          <Box width={"50%"}>
            Average Tempo: {averageTempo}
            <ReactSlider
              className="slider"
              thumbClassName="slider-thumb"
              trackClassName="slider-track"
              defaultValue={averageTempo}
              min={10}
              max={240}
              step={10}
              onChange={value => setAverageTempo(value)}
            />
            Tempo % Accuracy: {tempoAccuracy}
            <ReactSlider
              className="slider"
              thumbClassName="slider-thumb"
              trackClassName="slider-track"
              defaultValue={tempoAccuracy}
              onChange={value => setTempoAccuracy(value)}
            />
            Tuning % Accuracy: {tuningAccuracy}
            <ReactSlider
              className="slider"
              thumbClassName="slider-thumb"
              trackClassName="slider-track"
              defaultValue={tuningAccuracy}
              onChange={value => setTuningAccuracy(value)}
            />
            Dynamics % Accuracy: {dynamicsAccuracy}
            <ReactSlider
              className="slider"
              thumbClassName="slider-thumb"
              trackClassName="slider-track"
              defaultValue={dynamicsAccuracy}
              onChange={value => setDynamicsAccuracy(value)}
            />
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

function DeleteGoalButton({goals, setGoals, selectedGoal, setSelectedGoal}) {
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
      <div
        className={selectedGoal === -1 ? "btn small delete disabled" : "btn small delete"}
        onClick={deleteGoal}
      >
        Delete Goal
      </div>
    </>
  );
}

export { AddGoalButton, DeleteGoalButton };