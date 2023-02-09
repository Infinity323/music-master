import { useNavigate } from 'react-router-dom';
import backArrow from '../assets/back_arrow.png'
import settingsIcon from '../assets/settings_icon.png'

export function BackButton() {
  const navigate = useNavigate();
  return (
    <div className="btn back" onClick={() => navigate("/")}>
      <img src={backArrow} alt="Back" width="60px"/>
    </div>
  );
}

export function SettingsButton() {
  const navigate = useNavigate();
  return (
    <div className="btn back" onClick={() => navigate("/")}>
      <img src={settingsIcon} alt="Settings" width="60px"/>
    </div>
  );
}