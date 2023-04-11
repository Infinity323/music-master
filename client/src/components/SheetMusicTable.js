import { useEffect, useState, useRef } from 'react';
import { baseUrl, style } from '../App';
import loading_gif from '../assets/images/loading_gif.gif'
import Modal from 'react-modal'
import Select from 'react-select';

function SheetMusicTable() {
  const [responseStatus, setResponseStatus] = useState(200);
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [items, setItems] = useState([]);
  const [selected, setSelected] = useState(-1);

  useEffect(() => {
    fetch(baseUrl + "/sheetmusic")
      .then(res => {
        setResponseStatus(res.status);
        return res.json();
      })
      .then(result => {
        setIsLoaded(true);
        setItems(result);
      })
      .catch(error => {
        // Network connection error
        setIsLoaded(true);
        setError(error);
      });
  }, []);

  function UploadButton() {    
    const [modalIsOpen, setModalIsOpen] = useState(false);
    const [title, setTitle] = useState("");
    const [composer, setComposer] = useState("");
    const [instrument, setInstrument] = useState("Piano");
    const [file, setFile] = useState(null);
    const inputRef = useRef();

    const instruments = [
      { name: "Piano" },
      { name: "Guitar" },
      { name: "Violin" },
      { name: "Flute" },
      { name: "Clarinet" },
      { name: "Trumpet" },
      { name: "Saxophone" }
    ];

    const backgroundColor = style.getPropertyValue('--bg-color');
    const borderColor = "rgba(1, 1, 1, 0.2)";
    const buttonColor = style.getPropertyValue('--btn-color');
    const textColor = style.getPropertyValue('--text-color');

    // Dropdown styles
    const styles = {
      control: (styles) => ({
        ...styles,
        backgroundColor: buttonColor,
        borderColor: "rgba(1, 1, 1, 0)",
        color: textColor,
        fontSize: 16,
        width: 200
      }),
      option: (styles) => {
        return {
          ...styles,
          backgroundColor: backgroundColor,
          color: textColor,
          fontSize: 16,
          width: 200
        };
      },
      singleValue: (styles) => {
        return {
          ...styles,
          color: textColor
        };
      },
      menu: (styles) => {
        return {
          ...styles,
          backgroundColor: backgroundColor,
          width: 200
        };
      }
    };

    function openModal() {
      setModalIsOpen(true);
    }
    function closeModal() {
      setModalIsOpen(false);
    }

    function postMusic() {
      const formData = new FormData();
      formData.append("title", title);
      formData.append("composer", composer);
      formData.append("instrument", instrument);
      formData.append("file", file);
      fetch(baseUrl + "/sheetmusic", {
        method: "POST",
        body: formData
      }).then((res) => res.json())
        .then((data) => setItems(items.concat(data)));
      closeModal();
    }

    return (
      <>
        <div className="btn medium" id="uploadMusic" onClick={openModal}>
          Upload
        </div>
        <Modal
          isOpen={modalIsOpen} onRequestClose={closeModal}
          className="modal" overlayClassName="modal-overlay"
        >
          Title
          <br/><input type="text" onChange={(e) => setTitle(e.target.value)}/><br/>
          Composer
          <br/><input type="text" onChange={(e) => setComposer(e.target.value)}/><br/>
          Instrument
          <Select
            options={instruments.map(item => ({label: item.name, value: item.name}))}
            styles={styles}
            maxMenuHeight={200}
            onChange={e => setInstrument(e.value)}
            defaultValue={{ label: "Piano", value: "Piano" }}
            isSearchable={false}
          />
          <br/>
          File Upload
          <br/>
          <label className="btn small">
            Choose File
            <input
              type="file"
              accept=".musicxml"
              onChange={() => setFile(inputRef.current.files[0])}
              ref={inputRef}/>
          </label>
          {file ? file.name : ""}
          <div
            className={title === "" || composer === "" || instrument === "" || file === null
              ? "btn medium disabled"
              : "btn medium"}
            id="submitForm"
            onClick={postMusic}
          >
            Submit
          </div>
          <div className="btn medium" id="closeForm" onClick={closeModal}>
            Cancel
          </div>
        </Modal>
      </>
    );
  }

  function DeleteButton() {
    const [modalIsOpen, setModalIsOpen] = useState(false);

    function deleteMusic() {
      fetch(baseUrl + "/sheetmusic/" + selected, {
        method: "DELETE"
      }).then(res => res.json());
      const index = items.findIndex(item => item.id === selected);
      items.splice(index, 1);
      setItems(items);
      setSelected(-1);
    }

    function openModal() {
      setModalIsOpen(true);
    }
    function closeModal() {
      setModalIsOpen(false);
    }

    return (
      <>
        <div
          className={selected === -1 ? "btn medium disabled" : "btn medium"}
          onClick={openModal}
          id="deleteMusic"
        >
          Delete
        </div>
        <Modal
          isOpen={modalIsOpen} onRequestClose={closeModal}
          className="modal small" overlayClassName="modal-overlay"
        >
          <p>
            Are you sure you want to delete?
            <br/>
            All associated practice history data will be lost. 
          </p>
          <p className="error">
            This action cannot be undone.
          </p>
          <div className="btn medium delete" id="submitForm" onClick={deleteMusic}>
            Delete
          </div>
          <div className="btn medium" id="closeForm" onClick={closeModal}>
            Cancel
          </div>
        </Modal>
      </>
    )
  }

  if (error || responseStatus >= 400) {
    return (
      <p className="error">
        SheetMusicTable failed to render.
        <br/>
        { responseStatus >= 400
          ? responseStatus < 500
            ? `Client-side error (bad request)` // 400-499
            : `Server-side error (Flask encountered an error)` // 500-599
          : `Could not connect to ${baseUrl} (is Flask running?)`
        }
      </p>
    );
  } else if (!isLoaded) {
    return (
      <img src={loading_gif} width="50px" alt="Loading..."/>
    );
  } else {
    return (
      <>
        <table>
          <div className="tbody">
            <tbody>
              <tr className="header">
                <th id="title">Title</th>
                <th id="composer">Composer</th>
                <th id="instrument">Instrument</th>
              </tr>
              {items.map(item => (
                <tr className={selected === item.id ? "data selected" : "data"}
                  key={item.id} onClick={() => {setSelected(item.id)}}>
                  <td>{item.title}</td>
                  <td>{item.composer}</td>
                  <td>{item.instrument}</td>
                </tr>
              ))}
            </tbody>
          </div>
          <tfoot>
            <tr>
              <td colSpan="3">
                <UploadButton/>
                <DeleteButton/>
              </td>
            </tr>
          </tfoot>
        </table>
      </>
    );
  }
}

export default SheetMusicTable;
