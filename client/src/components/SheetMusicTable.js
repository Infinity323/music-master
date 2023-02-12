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
  }, [])

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

    // TODO: CRUD
    return (
      <>
        <div className="btn medium" id="uploadMusic" onClick={openModal}>
          Upload
        </div>
        <Modal isOpen={modalIsOpen} onRequestClose={closeModal}>
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
          <div className="btn medium" id="submitForm" onClick={closeModal}>
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
    // TODO: CRUD
    return (
      <>
        <div className={selected === -1 ? "btn medium disabled" : "btn medium"}
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
                <th width="120px">Instrument</th>
              </tr>
              {items.map(item => (
                <tr className={selected === item.id ? "data selected" : "data"}
                  key={item.id} onClick={() => {setSelected(item.id)}}>
                  <td>{item.title}</td>
                  <td>---</td>
                  <td>---</td>
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
