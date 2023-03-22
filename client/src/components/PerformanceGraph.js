import React, { Component } from 'react';
import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { BackButton } from '../components/Buttons';
import { baseUrl } from '../App';
import loading_gif from '../assets/images/loading_gif.gif'
import { useNavigate } from 'react-router-dom';
import data from '../assets/dat/270794_Test_5.json';
import { MDBDataTable } from 'mdbreact';


class PerformanceGraph extends Component {
   
    render() {
      return (
        <>
        <div className="App">
      <table>
        <tr>
          <th>Pitch</th>
          <th>Start</th>
          <th>End</th>
        </tr>
        {data.notes.map((notes, i) => (
            <tr key={i}>
                <td>{notes.pitch}</td>
                <td>{notes.start}</td>
                <td>{notes.end}</td>
            </tr>
        ))}
      </table>
    </div>
        </>
      );
    }
  }
    
export default PerformanceGraph;