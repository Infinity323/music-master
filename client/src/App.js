import { useState } from 'react';
import { useLocation, useOutlet } from 'react-router-dom';
import { CSSTransition, SwitchTransition } from 'react-transition-group';
import { routes } from './index';
import './App.css';
import { BpmContext, SheetMusicIdContext, ThemeContext, TunerContext } from './utils/Contexts';
import PerformanceGraph from './components/PerformanceGraph';

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
  const [bpm, setBpm] = useState(100);

  return (
    <div className="App">
      <PerformanceGraph></PerformanceGraph>
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
