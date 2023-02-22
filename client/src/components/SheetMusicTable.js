import { useEffect, useState } from 'react';
import { baseUrl } from '../App';
import loading_gif from '../assets/images/loading_gif.gif'
import Modal from 'react-modal'

function SheetMusicTable() {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [items, setItems] = useState([]);
  const [selected, setSelected] = useState(-1);

  useEffect(() => {
    fetch(baseUrl + "/sheetmusic")
      .then(res => res.json())
      .then(
        (result) => {
          setIsLoaded(true);
          setItems(result);
        },
        (error) => {
          setIsLoaded(true);
          setError(error);
        }
      )
  }, []);
  
  function deleteMusic() {
    fetch(baseUrl + "/sheetmusic/" + selected, {
      method: "DELETE"
    }).then((res) => res.json());
    const index = items.findIndex(item => item.id === selected);
    items.splice(index, 1);
    setItems(items);
    setSelected(-1);
  }

  function UploadButton() {    
    const [modalIsOpen, setModalIsOpen] = useState(false);
    const [title, setTitle] = useState("");
    const [composer, setComposer] = useState("");
    const [instrument, setInstrument] = useState("");
    const [file, setFile] = useState("");

    function openModal() {
      setModalIsOpen(true);
    }
    function closeModal() {
      setModalIsOpen(false);
    }

    function postMusic() {
      fetch(baseUrl + "/sheetmusic", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          "title": title,
          "composer": composer,
          "instrument": instrument,
          "pdf_file_path": file
        })
      }).then((res) => res.json())
        .then((data) => setItems(items.concat(data)));
      closeModal();
    }

    return (
      <>
        <div className="btn medium" id="uploadMusic" onClick={openModal}>
          Upload
        </div>
        <Modal isOpen={modalIsOpen} onRequestClose={closeModal} className="modal" overlayClassName="modal-overlay">
          Title: {title}
          <br/><input type="text" onChange={(e) => setTitle(e.target.value)}/><br/>
          Composer: {composer}
          <br/><input type="text" onChange={(e) => setComposer(e.target.value)}/><br/>
          Instrument: {instrument}
          <br/><input type="text" onChange={(e) => setInstrument(e.target.value)}/><br/>
          File Upload: {file}
          <br/>
          <label className="btn small">
            Choose File
            <input type="file" onChange={(e) => setFile(e.target.value)}/>
          </label>
          <br/>
          <div className="btn medium" id="submitForm" onClick={postMusic}>
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
    return (
      <>
        <div className={selected === -1 ? "btn medium disabled" : "btn medium"} onClick={deleteMusic}
          id="deleteMusic">Delete</div>
      </>
    )
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
        <img src={loading_gif} width="50px" alt="Loading..."/>
      </div>
    );
  } else {
    return (
      <>
        <table>
          <div className="tbody">
            <tbody>
              <tr className="header">
                <th width="400px">Title</th>
                <th width="150px">Composer</th>
                <th width="150px">Instrument</th>
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
