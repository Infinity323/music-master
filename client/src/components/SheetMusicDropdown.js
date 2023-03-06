import { useContext, useEffect, useState } from 'react';
import Select from 'react-select'
import { baseUrl, SheetMusicIdContext } from '../App';
import loading_gif from '../assets/images/loading_gif.gif'
import { style } from '../App';

function SheetMusicDropdown() {
  const styles = {
    control: (styles) => ({
      ...styles,
      backgroundColor: style.getPropertyValue('--btn-color'),
      color: style.getPropertyValue('--text-color'),
      fontSize: 16,
      width: 300
    }),
    option: (styles) => {
      return {
        ...styles,
        backgroundColor: style.getPropertyValue('--bg-color'),
        color: style.getPropertyValue('--text-color'),
        fontSize: 16,
        width: 300
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
        width: 300
      };
    }
  };

  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [items, setItems] = useState([]);
  const [selected, setSelected] = useContext(SheetMusicIdContext);
  
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
      );
  }, []);

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
        <Select
          options={items.map(item => ({label: item.title, value: item.id}))}
          styles={styles}
          maxMenuHeight={300}
          onChange={e => setSelected(e.value)}
          defaultValue={{
            label: selected === -1 ? "Select..." : items.find(item => item.id === selected).title,
            value: selected
          }}
          isSearchable={false}
        />
      </>
    );
  }
}

export default SheetMusicDropdown;