import { useEffect, useState } from 'react';
import { baseUrl } from '../App';
import loading_gif from '../assets/loading_gif.gif'

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
    // TODO: CRUD
    return (
      <>
        <div className="btn medium" id="uploadMusic">Upload</div>
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
        Error: {error.message}
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
          <tbody>
            <tr className="header">
              <th width="400px">Title</th>
              <th width="150px">Composer</th>
              <th width="120px">Instrument</th>
            </tr>
            {items.map(item => (
              <tr className={selected === item.id ? "selected" : "data"}
                key={item.id} onClick={() => {setSelected(item.id)}}>
                <td>{item.title}</td>
                <td>---</td>
                <td>---</td>
              </tr>
            ))}
          </tbody>
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
