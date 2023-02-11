import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import backArrow from '../assets/back_arrow.png'
import settingsIcon from '../assets/settings_icon.png'
import lightMode from '../assets/light_mode.png'
import darkMode from '../assets/dark_mode.png'
import highContrast from '../assets/high_contrast.png'

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
  const { style } = document.documentElement;

  function setLightMode() {

  }

  function setDarkMode() {
    style.setProperty('--bg-color', 'gray');
    style.setProperty('--text-color', 'white');
  }

  function setHighContrastMode() {

  }
  
  return (
    <div className={clicked ? "btn settings expanded" : "btn settings"}onClick={() => setClicked(!clicked)}>
      <img src={settingsIcon} alt="Settings" width="60px"/>
      <div class="settings-menu">
        <img src={lightMode} alt="Settings" width="60px" onClick={() => setLightMode()}/>
        <img src={darkMode} alt="Settings" width="60px" onClick={() => setDarkMode()}/>
        <img src={highContrast} alt="Settings" width="60px" onClick={() => setHighContrastMode()}/>
      </div>
    </div>
  );
}