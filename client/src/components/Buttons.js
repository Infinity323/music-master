import { useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import backArrow from '../assets/images/back_arrow.png';
import backArrowWhite from '../assets/images/back_arrow_white.png';
import home from '../assets/images/home.png';
import homeWhite from '../assets/images/home_white.png';
import lightMode from '../assets/images/light_mode.png';
import darkMode from '../assets/images/dark_mode.png';
import chart from '../assets/images/chart.png';
import chartWhite from '../assets/images/chart_white.png';
import { style } from '../App';
import { ThemeContext } from '../utils/Contexts';

export function BackButton() {
  const theme = useContext(ThemeContext)[0];
  const navigate = useNavigate();

  useEffect(() => {
    // Preload images
    const imageList = [backArrow, backArrowWhite];
    imageList.forEach(image => {
      new Image().src = image;
    });
  }, []);

  return (
    <div className="btn back" onClick={() => navigate(-1)}>
      <img
        src={theme === "light" ? backArrow : backArrowWhite}
        className="corner"
        alt="Back"/>
    </div>
  );
}

export function HomeButton() {
  const theme = useContext(ThemeContext)[0];
  const navigate = useNavigate();

  useEffect(() => {
    // Preload images
    const imageList = [home, homeWhite];
    imageList.forEach(image => {
      new Image().src = image;
    });
  }, []);

  return (
    <div className="btn back" onClick={() => navigate("/")}>
      <img
        src={theme === "light" ? home : homeWhite}
        className="corner"
        alt="Home"/>
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
    style.setProperty('--bg-color', '#E8EAF6');
    style.setProperty('--text-color', 'black');
    style.setProperty('--btn-color', '#C5CAE9');
    style.setProperty('--hover-color', '#9FA8DA');
    style.setProperty('--select-color', '#5C6BC0');
    style.setProperty('--hover-shadow-color', 'rgba(1, 1, 1, 0.2)');
  }

  function setDarkMode() {
    style.setProperty('--bg-color', '#313131');
    style.setProperty('--text-color', 'gainsboro');
    style.setProperty('--btn-color', '#414141');
    style.setProperty('--hover-color', '#525252');
    style.setProperty('--select-color', '#5C6BC0');
    style.setProperty('--hover-shadow-color', 'white');
  }

  function toggleTheme() {
    if (theme === "light") setTheme("dark");
    else setTheme("light");
  }
  
  useEffect(() => {
    // Preload images
    const imageList = [lightMode, darkMode];
    imageList.forEach(image => {
      new Image().src = image;
    });
    setProperties();
  }, []);

  useEffect(() => {
    if (theme === "dark") setDarkMode();
    else setLightMode();
  }, [theme]);
  
  return (
    <div className="btn settings" onClick={toggleTheme}>
      { theme === "dark"
        ? <img src={darkMode} className="corner" alt="Dark"/>
        : <img src={lightMode} className="corner" alt="Light"/>
      }
    </div>
  );
}

export function ChartButton() {
  const theme = useContext(ThemeContext)[0];
  const navigate = useNavigate();

  useEffect(() => {
    // Preload images
    const imageList = [chart, chartWhite];
    imageList.forEach(image => {
      new Image().src = image;
    });
  }, []);

  return (
    <div className="btn back" onClick={() => navigate("/history")}>
      <img
        src={theme === "light" ? chart : chartWhite}
        className="corner"
        alt="Chart"/>
    </div>
  );
}