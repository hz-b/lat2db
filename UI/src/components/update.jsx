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
  fetchQuadrupoles,
  updateQuadrupole,
  get_quad_from_seq,
  fetchMachineGroups,
  fetchMachineGroupElements,
  updateSextupole
} from "../APIs/machine_get_api";
import $ from "jquery";
import "select2/dist/js/select2.min.js";
import Swal from "sweetalert2";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPen } from "@fortawesome/free-solid-svg-icons";

const MyComponent = () => {
  const [machines, setMachines] = useState([]);
  const [quadrupoles, setQuadrupoles] = useState([]);
  const [selectedMachine, setSelectedMachine] = useState("");
  const [selectedQuad, setSelectedQuad] = useState(null);

  const [showRow, setShowRow] = useState(false);
  const [quadrupolesFetched, setQuadrupolesFetched] = useState(false);

  const [formData, setFormData] = useState({
    updateLength: '',
    updateCorrector: '',
    updateKickangleX: '',
    updateKickangleY: '',
    updatesnormal_coefficients: '',
    //updatenormal_coefficientsY: '',
    updateskew_coefficients: '',
    //updateskew_coefficientsY: '',
    updateMainMultipoleIndex: '',
    updateMainMultipoleStrenght: '',
    passMethod: '',
    tags: '',
    index: -1
  });


  const [updatedLength, setUpdatedLength] = useState("");
  const [updatedMethod, setUpdatedMethod] = useState("");
  const [updatedIntegrationSteps, setUpdatedIntegrationSteps] = useState("");
  const [updatedMultipleStrength, setUpdatedMultipleStrength] = useState("");
  const [updatedmMltipoleIndex, setUpdatedMltipoleIndex] = useState("");
  const [updatedName, setUpdatedName] = useState("");
  const [updatedType, setUpdatedType] = useState("");
  const [updatedIndex, setUpdatedIndex] = useState("");

  const [qud_for_radios, setQud_for_radios] = useState([]);
  const [selected_drift_RadioOption, setSelected_drift_RadioOption] =
    useState("");

  const [showModal, setShowModal] = useState(false);
  const [groups, setGroups] = useState([]);

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


  const handleMachingeddlChange = (event) => {
    let selectedMachineId;
    if (typeof event === "string") {
      selectedMachineId = event;
      setSelectedMachine(event);
    } else {

      selectedMachineId = event.target.value.toString();
      setSelectedMachine(selectedMachineId);
    }
    const fetchMahchineGroups = async (selectedMachine) => {
      try {
        const groupData = await fetchMachineGroups(selectedMachineId);
        console.log("groups are ", groupData)
        setGroups(groupData);
      } catch (error) {
        console.error("Error fetching quadrupoles:", error);
      }

    }

    fetchMahchineGroups(selectedMachineId);

  }

  const handleDDLGroupChange = (event) => { 


    const fetchQuadrupoles_func = async (MachineId,event) => {
      try {
        const quadrupolesData = await fetchMachineGroupElements(MachineId,event);
        console.log("the quad details are ...", quadrupolesData)
        
        setQuadrupoles(quadrupolesData);

       // setQuadrupolesFetched(true);
      } catch (error) {
        console.error("Error fetching quadrupoles:", error);
      }
    };

    fetchQuadrupoles_func(selectedMachine,event.target.value)

    // why the set state is not called 
    // console.log("wainting for the machine id ", selectedMachineId)
    // if (selectedMachineId) {
    //   console.log("called the quad all func")

    //   fetchQuadrupoles_func(selectedMachineId);
    // }


  };

  const handleQuadChange = async (event) => {

    var quadDetails;

    // console.log("update the event ",event)

    // if (typeof event === "number") {
    //   console.log("2", event)
    //   quadDetails = quadrupoles.find(
    //     (quad) => quad.index === parseInt(event)
    //   );
    //   setSelectedQuad(quadDetails);
    // } 
    // else {
    //   if (event != "") {
        const selectedQuadIndex = event.target.value;
        console.log("the selected index is after quad update",selectedQuadIndex)
        quadDetails = quadrupoles.find(
          (quad) => quad.index === parseInt(selectedQuadIndex)
        );
        
        console.log("quaddetailsare",quadrupoles)
        setSelectedQuad(quadDetails);
     // }
    //}




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

  useEffect(() => {
    if (selectedQuad) {
      setFormData({
        updateLength: selectedQuad.length?.toString() || '',
        updateCorrector: selectedQuad.element_configuration?.correctors?.toString() || '',
    
        updateKickangleX: selectedQuad.element_configuration?.kickangle?.x?.toString() || '0',
        updateKickangleY: selectedQuad.element_configuration?.kickangle?.y?.toString() || '0',
    
        updatesnormal_coefficients: selectedQuad.element_configuration?.magnetic_element?.coeffs?.normal_coefficients?.toString() || '0',
    
        updateskew_coefficients: selectedQuad.element_configuration?.magnetic_element?.coeffs?.skew_coefficients?.toString() || '0',
    
        updateMainMultipoleIndex: selectedQuad.element_configuration?.magnetic_element?.main_multipole_index?.toString() || '0',
        updateMainMultipoleStrenght: selectedQuad.element_configuration?.magnetic_element?.main_multipole_strength?.toString() || '0',
        passMethod: selectedQuad.passmethod?.toString() || '',
        tags: selectedQuad.tags?.toString() || '',
    
        index: selectedQuad.index?.toString() || '',
        name: selectedQuad.name?.toString() || ''
      });
    }
  }, [selectedQuad]);


  const handleInputChange = (e) => {
    console.log("e.target is ", e.target.value)
    const { id, value } = e.target;
    setFormData({
      ...formData,
      [id]: value
    });
  };


  const handleUpdateQuad = async () => {


    if (formData.updateLength !== selectedQuad.length.toString()) {
      if (showRow && !selected_drift_RadioOption) {
        Swal.fire({
          icon: "warning",
          title: "Select Quadrupole Option",
          text: "Please select a drift option before updating.",
        });
        setSelected_drift_RadioOption(-1)
        return;
      }
    }

    if (selectedQuad) {
      //console.log("update data is  ", formData)
      //setQuadrupolesFetched(false);

      try { 
        var newQuads;
        if(selectedQuad.type=="Quadrupole"){
           newQuads=await updateQuadrupole(
            selectedMachine,
            selectedQuad.name,
            selected_drift_RadioOption,
            formData,
            0
          );
        }else if(selectedQuad.type=="Sextupole"){

           newQuads=await updateSextupole(
            selectedMachine,
            selectedQuad.name,
            selected_drift_RadioOption,
            formData,
            0
          );
        }
       

        var quadDetails = newQuads.data.find(
          (quad) => quad.index === parseInt(selectedQuad.index)
        );
        if(newQuads){
          setSelectedQuad(quadDetails);
        }
        
        
        //handleMachineChange(selectedMachine)
        //console.log('1')
        //handleDDLGroupChange(selectedMachine)
        //console.log('selected quad index ',selectedQuad.index)
        //setQuadrupoles(await fetchQuadrupoles(selectedMachine));
        //if (quadrupolesFetched) {
        //  console.log('3........')
          ///handleQuadChange(selectedQuad ? selectedQuad.index : "")
        //  console.log("Quadrupole updated successfully");
          toggleModal();

          Swal.fire({
            icon: "success",
            title: "Quadrupole Updated",
            text: "The quadrupole parameters have been successfully updated.",
          });
        //}
      } catch (error) {
        console.error("Error updating quadrupole:", error);
        Swal.fire({
          icon: "error",
          title: "Error",
          text: "An error occurred while updating the quadrupole. Please try again.",
        });
      }
    }
  };

  const handleUpdateQuad_copy = async () => {


    if (formData.updateLength !== selectedQuad.length.toString()) {
      if (showRow && !selected_drift_RadioOption) {
        Swal.fire({
          icon: "warning",
          title: "Select Quadrupole Option",
          text: "Please select a drift option before updating.",
        });
        setSelected_drift_RadioOption(-1)
        return;
      }
    }

    if (selectedQuad) {
      //console.log("update data is  ", formData)
      //setQuadrupolesFetched(false);

      try {

        if(selectedQuad.type=="Quadrupole"){
          await updateQuadrupole(
            selectedMachine,
            selectedQuad.name,
            selected_drift_RadioOption,
            formData,
            1
          );
        }else if(selectedQuad.type=="Quadrupole"){

          const newQuads=await updateSextupole(
            selectedMachine,
            selectedQuad.name,
            selected_drift_RadioOption,
            formData,
            1
          );
        }
      

        // var quadDetails = newQuads.data.find(
        //   (quad) => quad.index === parseInt(selectedQuad.index)
        // );
        // if(newQuads){
        //   setSelectedQuad(quadDetails);
        // }
        //console.log("fethc value is ..", quadrupolesFetched)
        //handleDDLGroupChange(selectedMachine)
        //handleMachineChange(selectedMachine)
        //setQuadrupoles(await fetchQuadrupoles(selectedMachine));
        //console.log("valeu are.... ", selectedQuad ? selectedQuad.index : "")
       // if (quadrupolesFetched) {
        //  handleQuadChange(selectedQuad ? selectedQuad.index : "")
        //  console.log("Quadrupole updated successfully");
          toggleModal();

          Swal.fire({
            icon: "success",
            title: "Quadrupole updation & Machine creation",
            text: "The quadrupole parameters have been successfully updated into the new machine.",
          });
        //}
      } catch (error) {
        console.error("Error updating quadrupole:", error);
        Swal.fire({
          icon: "error",
          title: "Error",
          text: "An error occurred while updating the quadrupole. Please try again.",
        });
      }
    }
  };

  // useEffect(() => {
  //   if (quadrupolesFetched) {
  //     handleQuadChange(selectedQuad ? selectedQuad.index : "");
  //   }
  // }, [quadrupolesFetched]);

  const resetUpdatedState = () => {
    setUpdatedLength("");
    setUpdatedMethod("");
    setUpdatedIntegrationSteps("");
    setUpdatedMultipleStrength("");
    setUpdatedMltipoleIndex("");
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
            <h1 className="heading-text">Select Machine and Elements</h1>
          </div>
        </Col>
      </Row >
      <Row className="mt-1">
        <Col md={6}>
          <Row>
            <Col md={3}>
              <Form.Group controlId="machineSelect">
                <Form.Label>Select a Machine:</Form.Label>
                <Form.Control
                  as="select"
                  onChange={handleMachingeddlChange}
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
            <Col md={3}>
              <Form.Group controlId="groupSelect">
                <Form.Label>Select a Group:</Form.Label>

                <Form.Control
                  as="select"
                  onChange={handleDDLGroupChange}
                  disabled={!selectedMachine}
                  
                >
                  <option value="">Select...</option>
                  {groups.map((name,index) => (
                       <option key={`${name}-${index}`} value={name}>
                       {name}
                     </option>
                  ))}
                </Form.Control>

              </Form.Group>
            </Col>
            <Col md={5}>
              <Form.Group controlId="quadSelect">
                <Form.Label>Select a Element:</Form.Label>

                <Form.Control
                  as="select"
                  onChange={handleQuadChange}
                  disabled={!selectedMachine}
                  value={selectedQuad ? selectedQuad.index : ""}
                >
                  <option value="">Select...</option>
                  {quadrupoles.map((quad,idx) => (
                     <option key={`${quad.index}-${idx}`} value={quad.index}>
                      {`${quad.type}-${quad.name} - ${quad.index}`}
                    </option>
                  ))}
                </Form.Control>

              </Form.Group>
            </Col>
          </Row>
        </Col>
        <Col md={6}>
          {selectedQuad && (
            <Card>
              <Card.Body>
                <Card.Title>
                  {" "}
                  <FontAwesomeIcon
                    icon={faPen}
                    onClick={toggleModal}
                    style={{ cursor: "pointer", marginRight: "60px" }}
                  />
                  Selected {selectedQuad?selectedQuad.type:"Element"} Details
                </Card.Title>
                <Card.Text className="text-left align-left">
                  <table className="table table-bordered text-left">
                    <tbody>
                    <tr>
                        <td>
                          <strong>Element Type:</strong>
                        </td>
                        <td>{selectedQuad.type}</td>
                      </tr>
                      <tr>
                        <td>
                          <strong>Name:</strong>
                        </td>
                        <td>{selectedQuad.name}</td>
                      </tr>
                      <tr>
                        <td>
                          <strong>Index:</strong>
                        </td>
                        <td>{selectedQuad.index}</td>
                      </tr>
                      <tr>
                        <td>
                          <strong>Length:</strong>
                        </td>
                        <td>{selectedQuad.length}</td>
                      </tr>
                      <tr>
                        <td>
                          <strong>Correctors:</strong>
                        </td>
                        <td>{JSON.stringify(selectedQuad?.element_configuration?.correctors||"no values")||"no values"}</td>
                      </tr>
                      <tr>
                        <td>
                          <strong>kickangle:</strong>
                        </td>
                        <td>X:{JSON.stringify(selectedQuad.element_configuration?.kickangle.x)},Y:{JSON.stringify(selectedQuad.element_configuration?.kickangle.y)}</td>
                      </tr>
                      <tr>
                        <td>
                          <strong>Normal Coefficients:</strong>
                        </td>
                        <td>{JSON.stringify(selectedQuad.element_configuration?.magnetic_element.coeffs.normal_coefficients) || "No value"}</td>
                      </tr>
                      <tr>
                        <td>
                          <strong>Skew Coefficients:</strong>
                        </td>
                        <td>{JSON.stringify(selectedQuad.element_configuration?.magnetic_element.coeffs.skew_coefficients) || "No value"}</td>
                      </tr>
                      <tr>
                        <td>
                          <strong>Main Multiple Index:</strong>
                        </td>
                        <td>{JSON.stringify(selectedQuad.element_configuration?.magnetic_element.main_multipole_index) || "No value"}</td>
                      </tr>
                      <tr>
                        <td>
                          <strong>Main Multiple Strenght:</strong>
                        </td>
                        <td>{selectedQuad.element_configuration?.magnetic_element.main_multipole_strength ? JSON.stringify(selectedQuad.element_configuration?.magnetic_element.main_multipole_strength) : "No value"}</td>
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
          <Modal.Title>update {selectedQuad?selectedQuad.type:""}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Row className="mb-3">
            <Form.Group controlId="quadSelect_radios">
              <Form.Label>Select Drift Option:</Form.Label>
              <div>
                <Form.Check
                  type="checkbox"
                  id="showRowCheckbox"
                  label="Show Drift Option to edit"
                  checked={showRow}
                  onChange={(e) => setShowRow(e.target.checked)}
                />
                {showRow && (
                  (() => {
                    let index = quadrupoles.findIndex((quad) => quad.name === formData.name);
                    let previousQuad = quadrupoles[index - 1];
                    let previous_index = parseInt(quadrupoles[index].index) - 1;
                    let nextQuad = quadrupoles[index + 1];
                    let next_index = parseInt(quadrupoles[index].index) + 1;
                    console.log("current quad index is ", index);
                    console.log("previous quad is ", previousQuad);
                    console.log("next quad is ", nextQuad);

                    return (
                      <>
                        {previousQuad && (
                          <Form.Check
                            type="radio"
                            id="drift1"
                            name="drift"
                            label={`Previous Drift on index (${previous_index})`}
                            value={previous_index}
                            checked={selected_drift_RadioOption === previous_index.toString()}
                            onChange={(e) => setSelected_drift_RadioOption(e.target.value)}
                          />
                        )}

                        {nextQuad && (
                          <Form.Check
                            type="radio"
                            id="drift2"
                            name="drift"
                            label={`Next Drift on index (${next_index})`}
                            value={next_index}
                            checked={selected_drift_RadioOption === next_index.toString()}
                            onChange={(e) => setSelected_drift_RadioOption(e.target.value)}
                          />
                        )}
                      </>
                    );
                  })()
                )}
              </div>


            </Form.Group>
          </Row>

          <Row>

            <Form.Group as={Col} md="6" size="sm" controlId="passMethod">
              <Form.Label> Pass Method:</Form.Label>
              <Form.Control
                type="text"

                value={selectedQuad ? formData.passMethod : ""}
                onChange={handleInputChange}
              />
            </Form.Group>

            <Form.Group as={Col} md="6" size="sm" controlId="tags">
              <Form.Label>Tags:</Form.Label>
              <Form.Control
                type="text"
                value={selectedQuad ? formData.tags : ""}
                onChange={handleInputChange}
              />
            </Form.Group>

          </Row>


          <Row>

            <Form.Group as={Col} md="6" size="sm" controlId="updateLength">
              <Form.Label> Length:</Form.Label>
              <Form.Control
                type="number"

                value={selectedQuad ? formData.updateLength : 0}
                onChange={handleInputChange}
              />
            </Form.Group>

            <Form.Group as={Col} md="6" size="sm" controlId="updateCorrector">
              <Form.Label>Correctors:</Form.Label>
              <Form.Control
                type="text"
                value={selectedQuad ? formData?.updateCorrector : ""}
                onChange={handleInputChange}
              />
            </Form.Group>

          </Row>

          <Row>
            <Form.Group as={Col} md="6" controlId="updateKickangleX">
              <Form.Label>Kickangle (X):</Form.Label>
              <Form.Control
                type="number"
                step="0.01"
                value={selectedQuad ? formData.updateKickangleX : 0}
                onChange={handleInputChange}
              />
            </Form.Group>

            <Form.Group as={Col} md="6" controlId="updateKickangleY">
              <Form.Label> (Y):</Form.Label>
              <Form.Control
                type="number"
                step="0.01"
                value={selectedQuad ? formData.updateKickangleY : 0}
                onChange={handleInputChange}
              />
            </Form.Group>
          </Row>
          <Row>
            <Form.Group as={Col} md="12" controlId="updatesnormal_coefficients">
              <Form.Label>Normal Coefficients (x) :separate each element with a (,)</Form.Label>
              <Form.Control
                type="text"
                value={selectedQuad ? formData.updatesnormal_coefficients : 0}
                onChange={handleInputChange}
              />
            </Form.Group>



          </Row>

          <Row>
            <Form.Group as={Col} md="12" controlId="updateskew_coefficients">
              <Form.Label>Skew Coefficients :separate each element with a (,)</Form.Label>
              <Form.Control
                type="text"
                value={selectedQuad ? formData.updateskew_coefficients : 0}
                onChange={handleInputChange}
              />
            </Form.Group>

          </Row>

          <Row>
            <Form.Group as={Col} md="6" controlId="updateMainMultipoleIndex">
              <Form.Label>main multiple index:</Form.Label>
              <Form.Control
                type="number"
                step="0.01"
                value={selectedQuad ? formData.updateMainMultipoleIndex : 0}
                onChange={handleInputChange}
              />
            </Form.Group>

            <Form.Group as={Col} md="6" controlId="updateMainMultipoleStrenght">
              <Form.Label>main multiple strenght:</Form.Label>
              <Form.Control
                type="number"
                step="0.01"
                value={selectedQuad ? formData.updateMainMultipoleStrenght : 0}
                onChange={handleInputChange}
              />
            </Form.Group>
          </Row>


        </Modal.Body>


        <Modal.Footer>
          <Button variant="secondary" onClick={toggleModal}>
            Close
          </Button>
          <Button variant="primary" onClick={handleUpdateQuad}>
            Update
          </Button>
          <Button variant="primary" onClick={handleUpdateQuad_copy}>
            Save with a different Machine
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
};

export default MyComponent;

