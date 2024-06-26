import React from 'react';
import { BrowserRouter as Router, Routes, Link, Route } from 'react-router-dom';
import Navbar from "./components/nav";
import './App.css';
import Home from "./components/machine"
import Sextupole from "./components/sextupoles"
import Drift from "./components/drifts"
import Marker from "./components/markers"
import AttributeManByChart from "./components/attribute-man-by-chart"
import AttributeManByDDL from "./components/attribute-man-by-ddl"
import Monitor from "./components/monitor"
import CircleSVG from "./components/cricle";
function App() {
  return (
    <div className="App">
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" exact element={<Home />} />
          <Route path="/sextupole" element={<Sextupole />} />
          <Route path="/drift" element={<Drift/>} />
          <Route path="/marker" element={<Marker/>} />
          <Route path="/monitor" element={<Monitor/>} />
          <Route path="/attribute-man-by-chart" element={<AttributeManByChart/>} />
          <Route path="/attribute-man-by-DDL" element={<AttributeManByDDL/>} />
          <Route path="/circle" element={<CircleSVG/>} />
        </Routes>

      </Router>
    </div>
  );
}

export default App;
