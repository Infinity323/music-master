import React, { createRef } from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import Home from './pages/Home';
import TunerMetronome from './pages/TunerMetronome';
import PracticeHistory from './pages/PracticeHistory';
import SheetMusic from './pages/SheetMusic';
import StartPracticeSession from './pages/StartPracticeSession';
import Recording from './pages/Recording';
import Performance from './pages/Performance';
import reportWebVitals from './reportWebVitals';
import { RouterProvider, createHashRouter } from 'react-router-dom';
import NotFound from './pages/NotFound';

export const routes = [
  { path: '/', element: <Home/>, nodeRef: createRef() },
  { path: '/tuner', element: <TunerMetronome/>, nodeRef: createRef() },
  { path: '/history', element: <PracticeHistory/>, nodeRef: createRef() },
  { path: '/sheetmusic', element: <SheetMusic/>, nodeRef: createRef() },
  { path: '/startpracticesession', element: <StartPracticeSession/>, nodeRef: createRef() },
  { path: '/recording', element: <Recording/>, nodeRef: createRef() },
  { path: '/performance/:performanceId', element: <Performance/>, nodeRef: createRef() },
  { path: '*', element: <NotFound/>, nodeRef: createRef() }
];

const router = createHashRouter([
  {
    path: '/',
    element: <App/>,
    children: routes.map((route) => ({
      index: route.path === '/',
      path: route.path === '/' ? undefined : route.path,
      element: route.element,
    })),
  },
])

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  // <React.StrictMode>
    <RouterProvider router={router}/>
  // </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
