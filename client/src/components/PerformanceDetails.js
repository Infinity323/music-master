import { useState, useEffect } from 'react';
import { Card, Container, Row, Col } from 'react-bootstrap';
import { baseUrl } from '../App';
import '../assets/css/PerformanceDetails.css'

function PerformanceDetails({ sheet_music_id, run_number }) {
  const [performanceDiffs, setPerformanceDiffs] = useState([]);

  useEffect(() => {
    const loadDiffData = async () => {
      try {
        const response = await fetch(baseUrl + `/performance/diff/${sheet_music_id}/${run_number}`);

        if (!response.ok) {
          throw new Error(`Error fetching diff data: ${response.statusText}`);
        }

        const data = await response.json();
        setPerformanceDiffs(data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    loadDiffData();
  }, [sheet_music_id, run_number]);

  const renderDiff = (diff) => {
    const { ideal_val, actual_val, diff_type } = diff.diff;
    const valueLabels = {
      pitch: 'Pitch',
      velocity: 'Velocity',
      start: 'Start',
      end: 'End',
    };

    if (diff_type === 'extra' || diff_type === 'missing') {
      return <span>Note is {diff_type}.</span>;
    }

    return (
      <>
        Ideal: {valueLabels[diff_type]} {ideal_val[diff_type].toFixed(2)}
        <br />
        Actual: {valueLabels[diff_type]} {actual_val[diff_type].toFixed(2)}
      </>
    );
  };

  return (
    <Container fluid>
      <Row>
        <Col>
          <h1>Performance Diffs</h1>
        </Col>
      </Row>
      <Row>
        {performanceDiffs.map((diff, index) => (
          <Col sm={12} md={6} key={index} className="cardWrapper">
            <Card className="customCard">
              <Card.Body>
                <Card.Title className="cardTitle">Note {index + 1}</Card.Title>
                <Card.Subtitle className="mb-2 text-muted cardSubtitle">
                  {diff.note_info.name} ({diff.note_info.type}) in Measure {diff.note_info.measure}, Position {diff.note_info.position}
                </Card.Subtitle>
                <Card.Text className="cardText">
                  {renderDiff(diff)}
                  <br />
                  Difference Type: {diff.diff.diff_type}
                </Card.Text>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
    </Container>
  );
}

export default PerformanceDetails;
