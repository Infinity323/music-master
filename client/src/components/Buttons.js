import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import backArrow from '../assets/images/back_arrow.png'
import settingsIcon from '../assets/images/settings_icon.png'
import lightMode from '../assets/images/light_mode.png'
import darkMode from '../assets/images/dark_mode.png'

const { style } = document.documentElement;

export function BackButton() {
  const navigate = useNavigate();
  return (
    <div className="btn back" onClick={() => navigate("/")}>
      <img src={backArrow} alt="Back" width="60px"/>
    </div>
  );
}

export function SettingsButton() {
  const [clicked, setClicked] = useState(false);

  function setLightMode() {
    style.setProperty('--bg-color', 'ghostwhite');
    style.setProperty('--text-color', 'black');
    style.setProperty('--btn-color', '#E8EBF7');
    style.setProperty('--hover-color', '#ACBED8');
    style.setProperty('--select-color', '#D78521');
  }

  function setDarkMode() {
    style.setProperty('--bg-color', '#313131');
    style.setProperty('--text-color', 'gainsboro');
    style.setProperty('--btn-color', '#414141');
    style.setProperty('--hover-color', '#525252');
    style.setProperty('--select-color', '#CA3E47');
  }
  
  return (
    <div className={clicked ? "btn settings expanded" : "btn settings"}onClick={() => setClicked(!clicked)}>
      <img src={settingsIcon} alt="Settings" width="60px"/>
      <div class="settings-menu">
        <img src={lightMode} alt="Settings" width="60px" onClick={() => setLightMode()}/>
        <img src={darkMode} alt="Settings" width="60px" onClick={() => setDarkMode()}/>
      </div>
    </div>
  );
}