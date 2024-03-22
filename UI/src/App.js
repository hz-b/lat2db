import React from 'react';
import { BrowserRouter as Router, Routes, Link, Route } from 'react-router-dom';
import Navbar from "./components/nav";
import './App.css';
import Home from "./components/machine"
import Sextupole from "./components/sextupoles"
import Drift from "./components/drifts"
import Marker from "./components/markers"
import Monitor from "./components/monitor"
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
        </Routes>

      </Router>
    </div>
  );
}

export default App;
