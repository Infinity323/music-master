import { useState } from 'react';
import Modal from 'react-modal'
import Select from 'react-select'
import { style } from '../App';

function PracticeHistoryGraphOptions({showGoals, toggleGoals, timeWindow, changeTimeWindow}) {
  const [showModal, setShowModal] = useState(false);

  const styles = {
    control: (styles) => ({
      ...styles,
      backgroundColor: style.getPropertyValue('--btn-color'),
      borderColor: "rgba(1, 1, 1, 0)",
      color: style.getPropertyValue('--text-color'),
      fontSize: 16,
      width: 250
    }),
    option: (styles) => {
      return {
        ...styles,
        backgroundColor: style.getPropertyValue('--bg-color'),
        color: style.getPropertyValue('--text-color'),
        fontSize: 16,
        width: 250
      };
    },
    singleValue: (styles) => {
      return {
        ...styles,
        color: style.getPropertyValue('--text-color')
      };
    },
    menu: (styles) => {
      return {
        ...styles,
        backgroundColor: style.getPropertyValue('--bg-color'),
        width: 250
      };
    }
  };

  const timeWindowOptions = [
    { value: "hour", label: "Past Hour" },
    { value: "few-hours", label: "Past Few Hours" },
    { value: "day", label: "Past Day" },
    { value: "few-days", label: "Past Few Days" },
    { value: "week", label: "Past Week" },
    { value: "month", label: "Past Month" },
    { value: "all", label: "All Time" }
  ];

  function showOptions() {
    setShowModal(true);
  }

  function hideOptions() {
    setShowModal(false);
  }

  return (
    <>
      <div className="btn small" onClick={showOptions}>
        Options
      </div>
      <Modal isOpen={showModal} onRequestClose={hideOptions} className="modal" overlayClassName="modal-overlay">
        <div
          className={showGoals ? "btn small selected" : "btn small"}
          style={{width: 200}}
          onClick={toggleGoals}
        >
          Toggle Goals
        </div>
        <div className="btn medium" id="closeForm" onClick={hideOptions}>
          Close
        </div>
        <br/>
        <br/>
        Adjust Display Range
        <Select
          options={timeWindowOptions}
          styles={styles}
          onChange={e => {changeTimeWindow(e.value)}}
          defaultValue={timeWindowOptions.find(e => { return e.value === timeWindow; })}
          isSearchable={false}
        />
      </Modal>
    </>
  );
}

export default PracticeHistoryGraphOptions;