import { useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import backArrow from '../assets/images/back_arrow.png'
import lightMode from '../assets/images/light_mode.png'
import darkMode from '../assets/images/dark_mode.png'
import { style } from '../App';
import { ThemeContext } from '../utils/Contexts';

export function BackButton() {
  const navigate = useNavigate();
  return (
    <div className="btn back" onClick={() => navigate(-1)}>
      <img src={backArrow} className="corner" alt="Back"/>
    </div>
  );
}

export function ThemeButton() {
  const [theme, setTheme] = useContext(ThemeContext); 

  function setProperties() {
    // Set default color values on first application load
    if (theme === "light") setLightMode();
    else setDarkMode();
  }

  function setLightMode() {
    style.setProperty('--bg-color', 'ghostwhite');
    style.setProperty('--text-color', 'black');
    style.setProperty('--btn-color', '#E8EBF7');
    style.setProperty('--hover-color', '#ACBED8');
    style.setProperty('--select-color', '#D78521');
    style.setProperty('--hover-shadow-color', 'rgba(1, 1, 1, 0.2)');
  }

  function setDarkMode() {
    style.setProperty('--bg-color', '#313131');
    style.setProperty('--text-color', 'gainsboro');
    style.setProperty('--btn-color', '#414141');
    style.setProperty('--hover-color', '#525252');
    style.setProperty('--select-color', '#CA3E47');
    style.setProperty('--hover-shadow-color', 'white');
  }

  function toggleTheme() {
    if (theme === "light") setTheme("dark");
    else setTheme("light");
  }
  
  useEffect(() => {
    setProperties();
  });

  useEffect(() => {
    if (theme === "dark") setDarkMode();
    else setLightMode();
  }, [theme]);
  
  return (
    <div className="btn settings" onClick={toggleTheme}>
      {
        theme === "dark"
          ? <img src={darkMode} className="corner" alt="Dark"/>
          : <img src={lightMode} className="corner" alt="Light"/>
      }
    </div>
  );
}