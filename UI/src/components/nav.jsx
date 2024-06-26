import React from 'react';
import { Navbar, Nav, Container } from 'react-bootstrap';
import { Link, useLocation } from 'react-router-dom';
import './menu.css'; 

function NavBar() {
  const location = useLocation();

  const getLinkClass = (path) => {
    return location.pathname === path ? 'nav-link active' : 'nav-link';
  };

  return (
    <Navbar className="navbar" data-bs-theme="light">
      <Container>
        <Navbar.Brand as={Link} to="/">BESYII</Navbar.Brand>
        <Nav className="me-auto">
          <Nav.Link as={Link} to="/" className={getLinkClass('/')}>Quadrupoles</Nav.Link>
          <Nav.Link as={Link} to="/sextupole" className={getLinkClass('/sextupole')}>Sextupoles</Nav.Link>
          <Nav.Link as={Link} to="/drift" className={getLinkClass('/drift')}>Drifts</Nav.Link>
          <Nav.Link as={Link} to="/marker" className={getLinkClass('/marker')}>Markers</Nav.Link>
          <Nav.Link as={Link} to="/monitor" className={getLinkClass('/monitor')}>Beam Position Monitors</Nav.Link>
          <Nav.Link as={Link} to="/attribute-man-by-chart" className={getLinkClass('/attribute-man-by-chart')}>Attribute Customizer by Chart</Nav.Link>
          <Nav.Link as={Link} to="/attribute-man-by-DDL" className={getLinkClass('/attribute-man-by-DDL')}>Attribute Customizer</Nav.Link>
        </Nav>
      </Container>
    </Navbar>
  );
}

export default NavBar;
