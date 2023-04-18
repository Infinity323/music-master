import { useState, useEffect } from 'react';
import { useLocation, useOutlet } from 'react-router-dom';
import { CSSTransition, SwitchTransition } from 'react-transition-group';
import axios from 'axios';
import { routes } from './index';
import './App.css';
import { BpmContext, SheetMusicIdContext, ThemeContext, TunerContext } from './utils/Contexts';
import loading_gif from './assets/images/loading_gif.gif'

export const baseUrl = "http://127.0.0.1:5000";

export const { style } = document.documentElement;

function App() {
  const location = useLocation();
  const currentOutlet = useOutlet();
  const { nodeRef } = routes.find((route) => route.path === location.pathname)
    ?? {};

  const [theme, setTheme] = useState("light");
  const [selectedMusic, setSelectedMusic] = useState(-1);
  const [currentNote, setCurrentNote] = useState(-1);
  const [bpm, setBpm] = useState(120);
  const [isBackendReady, setIsBackendReady] = useState(false);

  useEffect(() => {
    async function fetchStatus() {
      const response = await axios.get(`${baseUrl}/status`);
      const status = response.data.status;
      if (status === 'ready') {
        setIsBackendReady(true);
      }
    }
    if (!isBackendReady) {
      let intervalId = setInterval(fetchStatus, 1000);
      return () => clearInterval(intervalId);
    }
  }, [isBackendReady]);

  if (!isBackendReady) {
    return (
      <div className="App">
        <div className="content">
          <h1>Music Master</h1>
          <h2>Loading...</h2>
          <img src={loading_gif} width="40px" alt="Loading..."/>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      <ThemeContext.Provider value={[theme, setTheme]}>
        <SheetMusicIdContext.Provider value={[selectedMusic, setSelectedMusic]}>
          <TunerContext.Provider value={[currentNote, setCurrentNote]}>
            <BpmContext.Provider value={[bpm, setBpm]}>
              <SwitchTransition>
                <CSSTransition
                  key={location.pathname}
                  nodeRef={nodeRef}
                  timeout={300}
                  classNames="page"
                  mountOnEnter={false}
                  unmountOnExit={true}
                >
                  {(state) => (
                    <div ref={nodeRef} className="page">
                      {currentOutlet}
                    </div>
                  )}
                </CSSTransition>
              </SwitchTransition>
            </BpmContext.Provider>
          </TunerContext.Provider>
        </SheetMusicIdContext.Provider>
      </ThemeContext.Provider>
    </div>
  );
}

export default App;
