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
  fetchDrifts,
  updateDrifts,

} from "../APIs/machine_get_api";
import $ from "jquery";
import "select2/dist/js/select2.min.js";
import Swal from "sweetalert2";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPen } from "@fortawesome/free-solid-svg-icons";

const MyComponent = () => {
  const [machines, setMachines] = useState([]);
  const [drifts, setDrifts] = useState([]);
  const [selectedMachine, setSelectedMachine] = useState("");
  const [selectedDrift, setSelectedDrift] = useState(null);

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
  const [driftFetched, setDriftsFetched] = useState(false);


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

    let selectedMachineId;
    if(typeof event==="string"){
      selectedMachineId=event;
      setSelectedMachine(event);
    }else{
    
     selectedMachineId = event.target.value.toString();
    console.log("geting the ",selectedMachineId)
    setSelectedMachine(selectedMachineId);
  }

    const fetchDrifts_func = async (selectedMachineId) => {
      try {
        const driftsData = await fetchDrifts(selectedMachineId);
        setDrifts(driftsData);

        setDriftsFetched(true);

      } catch (error) {
        console.error("Error fetching quadrupoles:", error);
      }
    };


  


    // why the set state is not called 
    if (selectedMachineId) {
      fetchDrifts_func(selectedMachineId);
    }


  };

  const handleDriftChange = async (event) => {

     var driftDetails;
   
     if (typeof event === "number") {
      driftDetails = drifts.find(
       (drift) => drift.index === parseInt(event)
     );
     setSelectedDrift(driftDetails);

      

     
    } else   { if (event!=""){
      const selectedDriftIndex = event.target.value;
      console.log(selectedDriftIndex)
       driftDetails = drifts.find(
        (drift) => drift.index === parseInt(selectedDriftIndex)
      );

      setSelectedDrift(driftDetails);
    }}







    if (driftDetails) {
      console.log("5")
      console.log("data is of the selected quad is ", driftDetails)
      setFormData({
        updateLength: driftDetails.length.toString(),

        passMethod: driftDetails.passmethod.toString(),
        tags: driftDetails.tags.toString(),

        index: driftDetails.index.toString(),
        name: driftDetails.name.toString(),


      });


      console.log("formdata data is after the drift fetching ", formData)
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


  const handleUpdateDrift = async () => {


    /*  if (formData.updateLength !== selectedDrift.length.toString()) {
       if (!selected_drift_RadioOption) {
         Swal.fire({
           icon: "warning",
           title:"Select Drift Option",
           text: "Please select a drift option before updating.",
         });
         setSelected_drift_RadioOption(-1)
         return;
       }
     } */

    if (selectedDrift) {
      console.log("calling the form data ", formData)
      setDriftsFetched(false)
      try {
        await updateDrifts(
          selectedMachine,
          selectedDrift.name,
          selected_drift_RadioOption,
          formData
        );
        

        handleMachineChange(selectedMachine)
        if (driftFetched) {
          handleDriftChange(selectedDrift ? selectedDrift.index : "")
          
          toggleModal();

          Swal.fire({
            icon: "success",
            title: "Drift Updated",
            text: "The drift parameters have been successfully updated.",
          });
        }

      } catch (error) {
        console.error("Error updating Drift:", error);
        Swal.fire({
          icon: "error",
          title: "Error",
          text: "An error occurred while updating the Drifts. Please try again.",
        });
      }
    }
  };

  useEffect(() => {
    if (driftFetched) {
      handleDriftChange(selectedDrift ? selectedDrift.index : "");
    }
  }, [driftFetched]);

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
    <Container className="mt-1">
      <Row>
        <Col>
          <div className="heading-container">
            <h1 className="heading-text">Select Machine and Drift</h1>
          </div>
        </Col>
      </Row >      <Row className="mt-1">
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
              <Form.Group controlId="driftSelect">
                <Form.Label>Select a Drift:</Form.Label>

                <Form.Control
                  as="select"
                  onChange={handleDriftChange}
                  disabled={!selectedMachine}
                  value={selectedDrift ? selectedDrift.index : ""}
                >
                  <option value="">Select...</option>
                  {drifts.map((drift, index) => (
                    <option key={index} value={drift.index}>
                      {`${drift.name} - ${drift.index}`}
                    </option>
                  ))}
                </Form.Control>

              </Form.Group>
            </Col>
          </Row>
        </Col>
        <Col md={6}>
          {selectedDrift && (
            <Card>
              <Card.Body>
                <Card.Title>
                  {" "}
                  <FontAwesomeIcon
                    icon={faPen}
                    onClick={toggleModal}
                    style={{ cursor: "pointer", marginRight: "60px" }}
                  />
                  Selected Drift Details
                </Card.Title>
                <Card.Text className="text-left align-left">
                  <table className="table table-bordered text-left">
                    <tbody>
                      <tr>
                        <td>
                          <strong>Name:</strong>
                        </td>
                        <td>{selectedDrift.name}</td>
                      </tr>
                      <tr>
                        <td>
                          <strong>Index:</strong>
                        </td>
                        <td>{selectedDrift.index}</td>
                      </tr>
                      <tr>
                        <td>
                          <strong>Length:</strong>
                        </td>
                        <td>{selectedDrift.length}</td>
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
          <Modal.Title>update Drifts</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {/*   <Row className="mb-3">
            <Form.Group controlId="sextSelect_radios">
              <Form.Label>Select Drift Option:</Form.Label>
              <div>
                {
                  (() => {
                    let index = drifts.findIndex((drift) => drift.name === formData.name);
                    let previousQuad = drifts[index - 1];
                    let nextQuad = drifts[index + 1];
                    console.log("current drift index is ", index);
                    console.log("previous drift is ", previousQuad);
                    console.log("next drift is ", nextQuad);

                    return (
                      <>
                        {previousQuad && (
                          <Form.Check
                            type="radio"
                            id="drift1"
                            name="drift"
                            label={`Previous drift (${previousQuad.name})`}
                            value={previousQuad.index}
                            checked={selected_drift_RadioOption === previousQuad.index.toString()}
                            onChange={(e) => setSelected_drift_RadioOption(e.target.value)}
                          />
                        )}

                        {nextQuad && (
                          <Form.Check
                            type="radio"
                            id="drift2"
                            name="drift"
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
          </Row> */}

          <Row>

            <Form.Group as={Col} md="6" size="sm" controlId="passMethod">
              <Form.Label> Pass Method:</Form.Label>
              <Form.Control
                type="text"

                value={selectedDrift ? formData.passMethod : ""}
                onChange={handleInputChange}
              />
            </Form.Group>

            <Form.Group as={Col} md="6" size="sm" controlId="tags">
              <Form.Label>Tags:</Form.Label>
              <Form.Control
                type="text"
                value={selectedDrift ? formData.tags : ""}
                onChange={handleInputChange}
              />
            </Form.Group>

          </Row>


          <Row>

            <Form.Group as={Col} md="6" size="sm" controlId="updateLength">
              <Form.Label> Length:</Form.Label>
              <Form.Control
                type="number"

                value={selectedDrift ? formData.updateLength : 0}
                onChange={handleInputChange}
              />
            </Form.Group>



          </Row>




        </Modal.Body>


        <Modal.Footer>
          <Button variant="secondary" onClick={toggleModal}>
            Close
          </Button>
          <Button variant="primary" onClick={handleUpdateDrift}>
            Update
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
};

export default MyComponent;

