import { useContext, useEffect, useState } from 'react';
import Select from 'react-select'
import { baseUrl, style } from '../App';
import loading_gif from '../assets/images/loading_gif.gif'
import { SheetMusicContext } from '../utils/Contexts';

function SheetMusicDropdown() {
  const backgroundColor = style.getPropertyValue('--bg-color');
  const borderColor = "rgba(1, 1, 1, 0.2)";
  const buttonColor = style.getPropertyValue('--btn-color');
  const textColor = style.getPropertyValue('--text-color');

  const styles = {
    control: (styles) => ({
      ...styles,
      backgroundColor: buttonColor,
      borderColor: "rgba(1, 1, 1, 0)",
      color: textColor,
      fontSize: 16,
      width: 300
    }),
    option: (styles) => {
      return {
        ...styles,
        backgroundColor: backgroundColor,
        color: textColor,
        fontSize: 16,
        width: 300
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
        width: 300
      };
    }
  };

  const [responseStatus, setResponseStatus] = useState(200);
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [sheetMusics, setSheetMusics] = useState([]);
  const [selected, setSelected] = useContext(SheetMusicContext);
  
  useEffect(() => {
    // Reset selected sheet music on render
    setSelected({
      id: -1,
      title: null,
      composer: null,
      instrument: null,
      pdf_file_path: null,
      data_file_path: null,
      tempo: null,
      note_info_file_path: null
    });
    // Fetch sheet music data from backend
    fetch(baseUrl + "/sheetmusic")
      .then(res => {
        setResponseStatus(res.status);
        return res.json();
      })
      .then(result => {
        setIsLoaded(true);
        setSheetMusics(result);
      })
      .catch(error => {
        // Network connection error
        setIsLoaded(true);
        setError(error);
      });
  }, []);

  if (error || responseStatus >= 400) {
    return (
      <p className="error">
        SheetMusicDropdown failed to render:
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
      <img src={loading_gif} width="30px" alt="Loading..."/>
    );
  } else {
    return (
      <>
        <Select
          options={sheetMusics.map(item => ({label: item.title, value: item}))}
          styles={styles}
          maxMenuHeight={300}
          onChange={e => setSelected(e.value)}
          defaultValue={{
            label: selected.id === -1 ? "Select..." : sheetMusics.find(item => item.id === selected.id).title,
            value: selected
          }}
          isSearchable={false}
        />
      </>
    );
  }
}

export default SheetMusicDropdown;