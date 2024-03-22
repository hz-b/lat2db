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
  fetchMonitor,
  updateMonitors,
  
} from "../APIs/machine_get_api";
import $ from "jquery";
import "select2/dist/js/select2.min.js";
import Swal from "sweetalert2";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPen } from "@fortawesome/free-solid-svg-icons";

const MyComponent = () => {
  const [machines, setMachines] = useState([]);
  const [monitors, setMonitors] = useState([]);
  const [selectedMachine, setSelectedMachine] = useState("");
  const [selectedMonitor, setSelectedMonitor] = useState(null);

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

    console.log("monitors is called .......", selectedMachine)
    const fetchMonitors_func = async (selectedMachineId) => {
      try {
        const monitorsData = await fetchMonitor(selectedMachineId);
        console.log("the monitor details are ...", monitorsData)
        setMonitors(monitorsData);


      } catch (error) {
        console.error("Error fetching monitors:", error);
      }
    };


    // why the set state is not called 
    if (selectedMachineId) {
      fetchMonitors_func(selectedMachineId);
    }


  };

  const handleMonitorChange = async (event) => {
    console.log("1")
    const selectedMonitorIndex = event.target.value;
    console.log("2")
    const monitorDetails = monitors.find(
      (monitor) => monitor.index === parseInt(selectedMonitorIndex)
    );
    console.log("3")
    setSelectedMonitor(monitorDetails);
    console.log("4")
    if (monitorDetails) {
      console.log("5")
      console.log("data is of the selected quad is ", monitorDetails)
      setFormData({
        updateLength: monitorDetails.length.toString(),
        
        passMethod: monitorDetails.passmethod.toString(),
        tags: monitorDetails.tags.toString(),

        index: monitorDetails.index.toString(),
        name: monitorDetails.name.toString(),


      });


      console.log("formdata data is after the monitor fetching ", formData)
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


  const handleUpdateMonitor = async () => {
  

    if (formData.updateLength !== selectedMonitor.length.toString()) {
      if (!selected_drift_RadioOption) {
        Swal.fire({
          icon: "warning",
          title:"Select Monitor Option",
          text: "Please select a monitor option before updating.",
        });
        setSelected_drift_RadioOption(-1)
        return;
      }
    }

    if (selectedMonitor) {
      console.log("calling the form data ", formData)
      try {
        await updateMonitors(
          selectedMachine,
          selectedMonitor.name,
          selected_drift_RadioOption,
          formData
        );

        setMonitors(await fetchMonitor(selectedMachine));
        console.log("Monitor updated successfully");
        toggleModal();

        Swal.fire({
          icon: "success",
          title: "Monitor Updated",
          text: "The Monitor parameters have been successfully updated.",
        });
      } catch (error) {
        console.error("Error updating Marker:", error);
        Swal.fire({
          icon: "error",
          title: "Error",
          text: "An error occurred while updating the Monitor. Please try again.",
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
              <Form.Group controlId="monitorSelect">
                <Form.Label>Select a Monitor:</Form.Label>

                <Form.Control
                  as="select"
                  onChange={handleMonitorChange}
                  disabled={!selectedMachine}
                  value={selectedMonitor ? selectedMonitor.index : ""}
                >
                  <option value="">Select...</option>
                  {monitors.map((monitor,index) => (
                    <option key={index} value={monitor.index}>
                      {`${monitor.name} - ${monitor.index}`}
                    </option>
                  ))}
                </Form.Control>

              </Form.Group>
            </Col>
          </Row>
        </Col>
        <Col md={6}>
          {selectedMonitor && (
            <Card>
              <Card.Body>
                <Card.Title>
                  {" "}
                  <FontAwesomeIcon
                    icon={faPen}
                    onClick={toggleModal}
                    style={{ cursor: "pointer", marginRight: "60px" }}
                  />
                  Selected Monitor Details
                </Card.Title>
                <Card.Text className="text-left align-left">
                  <table className="table table-bordered text-left">
                    <tbody>
                      <tr>
                        <td>
                          <strong>Name:</strong>
                        </td>
                        <td>{selectedMonitor.name}</td>
                      </tr>
                      <tr>
                        <td>
                          <strong>Index:</strong>
                        </td>
                        <td>{selectedMonitor.index}</td>
                      </tr>
                      <tr>
                        <td>
                          <strong>Length:</strong>
                        </td>
                        <td>{selectedMonitor.length}</td>
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
          <Modal.Title>update Monitor</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Row className="mb-3">
            <Form.Group controlId="sextSelect_radios">
              <Form.Label>Select marker Option:</Form.Label>
              <div>
                {
                  (() => {
                    let index = monitors.findIndex((monitor) => monitor.name === formData.name);
                    let previousQuad = monitors[index - 1];
                    let nextQuad = monitors[index + 1];
                    console.log("current monitor index is ", index);
                    console.log("previous monitor is ", previousQuad);
                    console.log("next monitor is ", nextQuad);
                    console.log("next monitor is on index 0 is ", monitors[0]);

                    return (
                      <>
                        {previousQuad && (
                          <Form.Check
                            type="radio"
                            id="monitor1"
                            name="monitor"
                            label={`Previous monitor (${previousQuad.name})`}
                            value={previousQuad.index}
                            checked={selected_drift_RadioOption === previousQuad.index.toString()}
                            onChange={(e) => setSelected_drift_RadioOption(e.target.value)}
                          />
                        )}

                        {nextQuad && (
                          <Form.Check
                            type="radio"
                            id="monitor2"
                            name="monitor"
                            label={`Next Monitor (${nextQuad.name})`}
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

                value={selectedMonitor ? formData.passMethod : ""}
                onChange={handleInputChange}
              />
            </Form.Group>

            <Form.Group as={Col} md="6" size="sm" controlId="tags">
              <Form.Label>Tags:</Form.Label>
              <Form.Control
                type="text"
                value={selectedMonitor ? formData.tags : ""}
                onChange={handleInputChange}
              />
            </Form.Group>

          </Row>


          <Row>

            <Form.Group as={Col} md="6" size="sm" controlId="updateLength">
              <Form.Label> Length:</Form.Label>
              <Form.Control
                type="number"

                value={selectedMonitor ? formData.updateLength : 0}
                onChange={handleInputChange}
              />
            </Form.Group>

         

          </Row>

        


        </Modal.Body>


        <Modal.Footer>
          <Button variant="secondary" onClick={toggleModal}>
            Close
          </Button>
          <Button variant="primary" onClick={handleUpdateMonitor}>
            Update
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
};

export default MyComponent;

