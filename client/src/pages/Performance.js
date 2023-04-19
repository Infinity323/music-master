import { useContext, useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { ChartButton } from '../components/Buttons';
import { baseUrl } from '../App';
import loading_gif from '../assets/images/loading_gif.gif'
import { useNavigate } from 'react-router-dom';
import PerformanceGraph from "../components/PerformanceGraph";
import PerformanceDetails from '../components/PerformanceDetails';
import { SheetMusicContext } from '../utils/Contexts';

export const options = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top',
    },
    title: {
      display: true,
      text: 'Performance Feedback',
    },
  },
};

function Performance() {
  const navigate = useNavigate();

  let { performanceId } = useParams();

  const [isLoaded, setIsLoaded] = useState(false);
  const [error, setError] = useState(null);
  const [performance, setPerformance] = useState(null);
  const sheetMusic = useContext(SheetMusicContext)[0];

  useEffect(() => {
    fetch(baseUrl + "/performance/" + performanceId)
      .then(res => res.json())
      .then(result => {
        setIsLoaded(true);
        setPerformance(result);
      })
      .catch(error => {
        setIsLoaded(false);
        setError(error);
      });
  }, []);

  function deletePerformance() {
    fetch(baseUrl + "/performance/" + performance.id, {
      method: "DELETE"
    }).then((res) => res.json());
    navigate(-1);
  }

  function DeleteButton() {
    return (
      <div className="btn small delete" onClick={deletePerformance}
        id="deletePerformance">Delete</div>
    );
  }

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
        <ChartButton/>
        <div className="content">
          <h2>Results for {sheetMusic.title}, Run #{performance.run_number}</h2>
          <PerformanceGraph performance={performance}/>
          <PerformanceDetails sheet_music_id={performance.sheet_music_id} run_number={performance.run_number} />
          <DeleteButton/>
        </div>
      </>
    );
  }
}

export default Performance;