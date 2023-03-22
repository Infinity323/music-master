import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { BackButton } from '../components/Buttons';
import { baseUrl } from '../App';
import loading_gif from '../assets/images/loading_gif.gif'
import { useNavigate } from 'react-router-dom';


function Performance() {
  const navigate = useNavigate();

  let { performanceId } = useParams();

  const [isLoaded, setIsLoaded] = useState(false);
  const [error, setError] = useState(null);
  const [performance, setPerformance] = useState(null);

  useEffect(() => {
    fetch(baseUrl + "/performance/" + performanceId)
      .then(res => res.json())
      .then(
        (result) => {
          setIsLoaded(true);
          setPerformance(result);
        },
        (error) => {
          setIsLoaded(false);
          setError(error);
        }
      )
  }, []);

  function deletePerformance() {
    fetch(baseUrl + "/performance/" + performance.id, {
      method: "DELETE"
    }).then((res) => res.json());
    navigate(-1);
  }

  function DeleteButton() {
    return (
      <>
        <div className="btn medium" onClick={deletePerformance}
          id="deletePerformance">Delete</div>
      </>
    )
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
        <BackButton/>
        <div className="content">
          Results for performance {performance.id}, sheet music {performance.sheet_music_id}
        </div>
        <DeleteButton/>
      </>
    );
  }
}

export default Performance;