import React from 'react'
import { Navbar,Nav,Form,Button,Badge } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import Container from 'react-bootstrap/Container';

function nav() {
  return (
    <Navbar bg="light" data-bs-theme="light">
      <Container>
        <Navbar.Brand as={Link} to="/">BESYII</Navbar.Brand>
        <Nav className="me-auto">
          <Nav.Link as={Link} to="/">Quadrupoles</Nav.Link>
          <Nav.Link as={Link} to="/sextupole">Sextupoles</Nav.Link>
          <Nav.Link as={Link} to="/drift">Drifts</Nav.Link>
          <Nav.Link as={Link} to="/marker">Markers</Nav.Link>
          <Nav.Link as={Link} to="/monitor">Beam Position Monitors</Nav.Link>
        </Nav>
      </Container>
    </Navbar>
  )
}

export default nav