// src/App.js
import React, { useState, useEffect } from 'react';
import LatticeRing from './components/LatticeRing';
import './App.css'; // Import the CSS file

const draftElements = [
  { type: 'quadrupole', index: 1, info: 'Quad 1' },
  { type: 'quadrupole', index: 2, info: 'Quad 2' },
  { type: 'sextupole', index: 3, info: 'Sext 1' },
  { type: 'drift', index: 4, info: 'Drift 1' },
  { type: 'monitor', index: 5, info: 'Monitor 1' },
  { type: 'quadrupole', index: 6, info: 'Quad 3' },
  { type: 'sextupole', index: 7, info: 'Sext 2' },
  { type: 'drift', index: 8, info: 'Drift 2' },
  { type: 'monitor', index: 9, info: 'Monitor 2' },
];

const App = () => {
  const [elements, setElements] = useState(draftElements);
  const [selectedElement, setSelectedElement] = useState(null);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    // Apply filter to elements
    if (filter === 'all') {
      setElements(draftElements);
    } else {
      const filteredElements = draftElements.filter(element => element.type === filter);
      setElements(filteredElements);
    }
  }, [filter]);

  const handleElementClick = (element) => {
    setSelectedElement(element);
  };

  return (
    <div className="container">
      <h1>Bessy II Visualization</h1>
      <div className="control-panel">
        <label htmlFor="filter">Filter Elements: </label>
        <select id="filter" value={filter} onChange={e => setFilter(e.target.value)}>
          <option value="all">All</option>
          <option value="quadrupole">Quadrupoles</option>
          <option value="sextupole">Sextupoles</option>
          <option value="drift">Drifts</option>
          <option value="monitor">Monitors</option>
        </select>
      </div>
      <LatticeRing elements={elements} onElementClick={handleElementClick} />
      {selectedElement && (
        <table className="element-table">
          <thead>
            <tr>
              <th>Field</th>
              <th>Value</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>Type</td><td>{selectedElement.type}</td></tr>
            <tr><td>Index</td><td>{selectedElement.index}</td></tr>
            <tr><td>Additional Info</td><td>{selectedElement.info}</td></tr>
          </tbody>
        </table>
      )}
    </div>
  );
};

export default App;
