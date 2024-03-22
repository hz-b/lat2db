import React, { useState, useEffect } from "react";
import {
  Container,
  Row,
  Col,
  Card,
  Button,
  Form,
  Modal
} from "react-bootstrap";
import {
  fetchMachines,
  fetchMarkers,
  updateMarkers,
  
} from "../APIs/machine_get_api";
import $ from "jquery";
import "select2/dist/js/select2.min.js";
import Swal from "sweetalert2";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPen } from "@fortawesome/free-solid-svg-icons";

const MyComponent = () => {
  const [machines, setMachines] = useState([]);
  const [markers, setMarkers] = useState([]);
  const [selectedMachine, setSelectedMachine] = useState("");
  const [selectedMarker, setSelectedMarker] = useState(null);

  const [formData, setFormData] = useState({
    updateLength: '',
    passMethod: '',
    tags: '',
    index: -1
  });


  const [updatedLength, setUpdatedLength] = useState("");
  const [updatedMethod, setUpdatedMethod] = useState("");
  const [updatedName, setUpdatedName] = useState("");
  const [updatedType, setUpdatedType] = useState("");
  const [updatedIndex, setUpdatedIndex] = useState("");

  const [qud_for_radios, setQud_for_radios] = useState([]);
  const [selected_drift_RadioOption, setSelected_drift_RadioOption] =
    useState("");

  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    // Fetch machines on component mount
    const fetchMachines_func = async () => {
      try {
        const machinesData = await fetchMachines();
        setMachines(machinesData);
      } catch (error) {
        console.error("Error fetching machines:", error);
      }
    };

    fetchMachines_func();
  }, []);


  const handleMachineChange = (event) => {


    const selectedMachineId = event.target.value.toString();
    setSelectedMachine(selectedMachineId);

    console.log("marker is called .......", selectedMachine)
    const fetchMarkers_func = async (selectedMachineId) => {
      try {
        const markersData = await fetchMarkers(selectedMachineId);
        console.log("the marker details are ...", markersData)
        setMarkers(markersData);


      } catch (error) {
        console.error("Error fetching markers:", error);
      }
    };


    // why the set state is not called 
    if (selectedMachineId) {
      fetchMarkers_func(selectedMachineId);
    }


  };

  const handleMarkerChange = async (event) => {
    console.log("1")
    const selectedMarkerIndex = event.target.value;
    console.log("2")
    const markerDetails = markers.find(
      (marker) => marker.index === parseInt(selectedMarkerIndex)
    );
    console.log("3")
    setSelectedMarker(markerDetails);
    console.log("4")
    if (markerDetails) {
      console.log("5")
      console.log("data is of the selected quad is ", markerDetails)
      setFormData({
        updateLength: markerDetails.length.toString(),
        
        passMethod: markerDetails.passmethod.toString(),
        tags: markerDetails.tags.toString(),

        index: markerDetails.index.toString(),
        name: markerDetails.name.toString(),


      });


      console.log("formdata data is after the marker fetching ", formData)
    }



    /*   if (quadDetails) {
        resetUpdatedState(); // Reset the state
        try {
          const qud_from_seq = await get_quad_from_seq(
            selectedMachine,
            quadDetails.name
          );
  
          setQud_for_radios(qud_from_seq);
  
          // Update state with the response
          setUpdatedLength(quadDetails.length.toString());
          setUpdatedMethod(quadDetails.method.toString());
          setUpdatedIntegrationSteps(
            quadDetails.number_of_integration_steps.toString()
          );
          setUpdatedMultipleStrength(
            quadDetails.main_multipole_strength.toString()
          );
          setUpdatedMltipoleIndex(quadDetails.main_multipole_index.toString());
          setUpdatedIndex(quadDetails.index.toString());
          setUpdatedType(quadDetails.type.toString());
          setUpdatedName(quadDetails.name.toString());
        } catch (error) {
          console.error("Error updating quadrupole:", error);
        }
      } */
  };

  const handleInputChange = (e) => {
    console.log("e.target is ", e.target.value)



    const { id, value } = e.target;
    setFormData({
      ...formData,
      [id]: value
    });
  };


  const handleUpdateMarker = async () => {
  

    if (formData.updateLength !== selectedMarker.length.toString()) {
      if (!selected_drift_RadioOption) {
        Swal.fire({
          icon: "warning",
          title:"Select Marker Option",
          text: "Please select a marker option before updating.",
        });
        setSelected_drift_RadioOption(-1)
        return;
      }
    }

    if (selectedMarker) {
      console.log("calling the form data ", formData)
      try {
        await updateMarkers(
          selectedMachine,
          selectedMarker.name,
          selected_drift_RadioOption,
          formData
        );

        setMarkers(await fetchMarkers(selectedMachine));
        console.log("Marker updated successfully");
        toggleModal();

        Swal.fire({
          icon: "success",
          title: "Marker Updated",
          text: "The Marker parameters have been successfully updated.",
        });
      } catch (error) {
        console.error("Error updating Marker:", error);
        Swal.fire({
          icon: "error",
          title: "Error",
          text: "An error occurred while updating the Markers. Please try again.",
        });
      }
    }
  };

  const resetUpdatedState = () => {
    setUpdatedLength("");
    setUpdatedMethod("");
   
    setUpdatedName("");
    setUpdatedType("");
    setUpdatedIndex("");
  };

  // Function to toggle modal visibility
  const toggleModal = () => {
    setShowModal(!showModal);
  };

  return (
    <Container className="mt-5">
      <Row>
        <Col md={6}>
          <Row>
            <Col md={6}>
              <Form.Group controlId="machineSelect">
                <Form.Label>Select a Machine:</Form.Label>
                <Form.Control
                  as="select"
                  onChange={handleMachineChange}
                  value={selectedMachine}
                >
                  <option value="">Select...</option>
                  {machines.map((machine) => (
                    <option key={machine.id} value={machine.id}>
                      {machine.name}
                    </option>
                  ))}
                </Form.Control>
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group controlId="markerSelect">
                <Form.Label>Select a Marker:</Form.Label>

                <Form.Control
                  as="select"
                  onChange={handleMarkerChange}
                  disabled={!selectedMachine}
                  value={selectedMarker ? selectedMarker.index : ""}
                >
                  <option value="">Select...</option>
                  {markers.map((marker,index) => (
                    <option key={index} value={marker.index}>
                      {`${marker.name} - ${marker.index}`}
                    </option>
                  ))}
                </Form.Control>

              </Form.Group>
            </Col>
          </Row>
        </Col>
        <Col md={6}>
          {selectedMarker && (
            <Card>
              <Card.Body>
                <Card.Title>
                  {" "}
                  <FontAwesomeIcon
                    icon={faPen}
                    onClick={toggleModal}
                    style={{ cursor: "pointer", marginRight: "60px" }}
                  />
                  Selected Marker Details
                </Card.Title>
                <Card.Text className="text-left align-left">
                  <table className="table table-bordered text-left">
                    <tbody>
                      <tr>
                        <td>
                          <strong>Name:</strong>
                        </td>
                        <td>{selectedMarker.name}</td>
                      </tr>
                      <tr>
                        <td>
                          <strong>Index:</strong>
                        </td>
                        <td>{selectedMarker.index}</td>
                      </tr>
                      <tr>
                        <td>
                          <strong>Length:</strong>
                        </td>
                        <td>{selectedMarker.length}</td>
                      </tr>
                   
                    </tbody>
                  </table>
                </Card.Text>
                {/*  <Button variant="primary" onClick={toggleModal}>
                  Update Quadrupole
                </Button> */}
              </Card.Body>
            </Card>
          )}
        </Col>
      </Row>

      {/* Modal for updating quadrupole */}
      <Modal show={showModal} onHide={toggleModal}>
        <Modal.Header closeButton>
          <Modal.Title>update Marker</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Row className="mb-3">
            <Form.Group controlId="sextSelect_radios">
              <Form.Label>Select marker Option:</Form.Label>
              <div>
                {
                  (() => {
                    let index = markers.findIndex((marker) => marker.name === formData.name);
                    let previousQuad = markers[index - 1];
                    let nextQuad = markers[index + 1];
                    console.log("current marker index is ", index);
                    console.log("previous marker is ", previousQuad);
                    console.log("next marker is ", nextQuad);

                    return (
                      <>
                        {previousQuad && (
                          <Form.Check
                            type="radio"
                            id="marker1"
                            name="marker"
                            label={`Previous marker (${previousQuad.name})`}
                            value={previousQuad.index}
                            checked={selected_drift_RadioOption === previousQuad.index.toString()}
                            onChange={(e) => setSelected_drift_RadioOption(e.target.value)}
                          />
                        )}

                        {nextQuad && (
                          <Form.Check
                            type="radio"
                            id="marker2"
                            name="marker"
                            label={`Next Drift (${nextQuad.name})`}
                            value={nextQuad.index}
                            checked={selected_drift_RadioOption === nextQuad.index.toString()}
                            onChange={(e) => setSelected_drift_RadioOption(e.target.value)}
                          />
                        )}
                      </>
                    );
                  })()
                }
              </div>


            </Form.Group>
          </Row>

          <Row>

            <Form.Group as={Col} md="6" size="sm" controlId="passMethod">
              <Form.Label> Pass Method:</Form.Label>
              <Form.Control
                type="text"

                value={selectedMarker ? formData.passMethod : ""}
                onChange={handleInputChange}
              />
            </Form.Group>

            <Form.Group as={Col} md="6" size="sm" controlId="tags">
              <Form.Label>Tags:</Form.Label>
              <Form.Control
                type="text"
                value={selectedMarker ? formData.tags : ""}
                onChange={handleInputChange}
              />
            </Form.Group>

          </Row>


          <Row>

            <Form.Group as={Col} md="6" size="sm" controlId="updateLength">
              <Form.Label> Length:</Form.Label>
              <Form.Control
                type="number"

                value={selectedMarker ? formData.updateLength : 0}
                onChange={handleInputChange}
              />
            </Form.Group>

         

          </Row>

        


        </Modal.Body>


        <Modal.Footer>
          <Button variant="secondary" onClick={toggleModal}>
            Close
          </Button>
          <Button variant="primary" onClick={handleUpdateMarker}>
            Update
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
};

export default MyComponent;

