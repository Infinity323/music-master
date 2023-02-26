import { useParams } from 'react-router-dom';
import { BackButton } from '../components/Buttons';

function Performance() {
  let { performanceId } = useParams();
  return (
    <>
      <BackButton/>
      <div className="content">
        Results for performance {performanceId}
      </div>
    </>
  );
}

export default Performance;