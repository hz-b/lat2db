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
  fetchSextupoles,
  updateSextupole,
  
} from "../APIs/machine_get_api";
import $ from "jquery";
import "select2/dist/js/select2.min.js";
import Swal from "sweetalert2";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPen } from "@fortawesome/free-solid-svg-icons";

const MyComponent = () => {
  const [machines, setMachines] = useState([]);
  const [sextupoles, setSextupoles] = useState([]);
  const [selectedMachine, setSelectedMachine] = useState("");
  const [selectedSext, setSelectedSext] = useState(null);
  const [showRow, setShowRow] = useState(false);

  const [formData, setFormData] = useState({
    updateLength: '',
    updateCorrector: '',
    updateKickangleX: '',
    updateKickangleY: '',
    updatesnormal_coefficientsX: '',
    updatenormal_coefficientsY: '',
    updateskew_coefficientsX: '',
    updateskew_coefficientsY: '',
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

    console.log("quad is called .......", selectedMachine)
    const fetchSextupoles_func = async (selectedMachineId) => {
      try {
        const sextupolesData = await fetchSextupoles(selectedMachineId);
        console.log("the quad details are ...", sextupolesData)
        setSextupoles(sextupolesData);


      } catch (error) {
        console.error("Error fetching sextupoles:", error);
      }
    };


    // why the set state is not called 
    if (selectedMachineId) {
      fetchSextupoles_func(selectedMachineId);
    }


  };

  const handleQuadChange = async (event) => {
    console.log("1")
    const selectedSextIndex = event.target.value;
    console.log("2")
    const sextDetails = sextupoles.find(
      (sext) => sext.index === parseInt(selectedSextIndex)
    );
    console.log("3")
    setSelectedSext(sextDetails);
    console.log("4")
    if (sextDetails) {
      console.log("5")
      console.log("data is of the selected quad is ", sextDetails)
      setFormData({
        updateLength: sextDetails.length.toString(),
        updateCorrector: sextDetails.element_configuration.correctors?.toString() ?? [],

        updateKickangleX: sextDetails.element_configuration.kickangle.x?.toString() ?? 0,
        updateKickangleY: sextDetails.element_configuration.kickangle.y?.toString() ?? 0,

        updatesnormal_coefficientsX: sextDetails.element_configuration.magnetic_element.coeffs.normal_coefficients[0]?.toString() ?? 0,
        updatenormal_coefficientsY: sextDetails.element_configuration.magnetic_element.coeffs.normal_coefficients[1]?.toString() ?? 0,

        updateskew_coefficientsX: sextDetails.element_configuration.magnetic_element.coeffs.skew_coefficients[0]?.toString() ?? 0,
        updateskew_coefficientsY: sextDetails.element_configuration.magnetic_element.coeffs.skew_coefficients[1]?.toString() ?? 0,


        updateMainMultipoleIndex: sextDetails.element_configuration.magnetic_element.main_multipole_index?.toString() ?? 0,
        updateMainMultipoleStrenght: sextDetails.element_configuration.magnetic_element.main_multipole_strength?.toString() ?? 0,
        passMethod: sextDetails.passmethod.toString(),
        tags: sextDetails.tags.toString(),

        index: sextDetails.index.toString(),
        name: sextDetails.name.toString(),


      });


      console.log("formdata data is after the quad fetching ", formData)
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


  const handleUpdateSext = async () => {
  

    if (formData.updateLength !== selectedSext.length.toString()) {
      if (showRow && !selected_drift_RadioOption) {
        Swal.fire({
          icon: "warning",
          title:"Select Quadrupole Option",
          text: "Please select a drift option before updating.",
        });
        setSelected_drift_RadioOption(-1)
        return;
      }
    }

    if (selectedSext) {
      console.log("calling the form data ", formData)
      try {
        await updateSextupole(
          selectedMachine,
          selectedSext.name,
          selected_drift_RadioOption,
          formData
        );

        setSextupoles(await fetchSextupoles(selectedMachine));
        console.log("Quadrupole updated successfully");
        toggleModal();

        Swal.fire({
          icon: "success",
          title: "Sextupole Updated",
          text: "The Sextupole parameters have been successfully updated.",
        });
      } catch (error) {
        console.error("Error updating quadrupole:", error);
        Swal.fire({
          icon: "error",
          title: "Error",
          text: "An error occurred while updating the Sextupoles. Please try again.",
        });
      }
    }
  };

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
        <h1 className="heading-text">Select Machine and Sextupoles</h1>
      </div>
    </Col>
  </Row >
      <Row className="mt-1">
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
              <Form.Group controlId="sextSelect">
                <Form.Label>Select a Sextupole:</Form.Label>

                <Form.Control
                  as="select"
                  onChange={handleQuadChange}
                  disabled={!selectedMachine}
                  value={selectedSext ? selectedSext.index : ""}
                >
                  <option value="">Select...</option>
                  {sextupoles.map((sext) => (
                    <option key={sext.index} value={sext.index}>
                      {`${sext.name} - ${sext.index}`}
                    </option>
                  ))}
                </Form.Control>

              </Form.Group>
            </Col>
          </Row>
        </Col>
        <Col md={6}>
          {selectedSext && (
            <Card>
              <Card.Body>
                <Card.Title>
                  {" "}
                  <FontAwesomeIcon
                    icon={faPen}
                    onClick={toggleModal}
                    style={{ cursor: "pointer", marginRight: "60px" }}
                  />
                  Selected Sextupoles Details
                </Card.Title>
                <Card.Text className="text-left align-left">
                  <table className="table table-bordered text-left">
                    <tbody>
                      <tr>
                        <td>
                          <strong>Name:</strong>
                        </td>
                        <td>{selectedSext.name}</td>
                      </tr>
                      <tr>
                        <td>
                          <strong>Index:</strong>
                        </td>
                        <td>{selectedSext.index}</td>
                      </tr>
                      <tr>
                        <td>
                          <strong>Length:</strong>
                        </td>
                        <td>{selectedSext.length}</td>
                      </tr>
                      <tr>
                        <td>
                          <strong>Correctors:</strong>
                        </td>
                        <td>{JSON.stringify(selectedSext.element_configuration.correctors)}</td>
                      </tr>
                      <tr>
                        <td>
                          <strong>kickangle:</strong>
                        </td>
                        <td>X:{JSON.stringify(selectedSext.element_configuration.kickangle.x)},Y:{JSON.stringify(selectedSext.element_configuration.kickangle.y)}</td>
                      </tr>
                      <tr>
                        <td>
                          <strong>Normal Coefficients:</strong>
                        </td>
                        <td>{JSON.stringify(selectedSext.element_configuration.magnetic_element.coeffs.normal_coefficients) || "No value"}</td>
                      </tr>
                      <tr>
                        <td>
                          <strong>Skew Coefficients:</strong>
                        </td>
                        <td>{JSON.stringify(selectedSext.element_configuration.magnetic_element.coeffs.skew_coefficients) || "No value"}</td>
                      </tr>
                      <tr>
                        <td>
                          <strong>Main Multiple Index:</strong>
                        </td>
                        <td>{JSON.stringify(selectedSext.element_configuration.magnetic_element.main_multipole_index) || "No value"}</td>
                      </tr>
                      <tr>
                        <td>
                          <strong>Main Multiple Strenght:</strong>
                        </td>
                        <td>{selectedSext.element_configuration.magnetic_element.main_multipole_strength ? JSON.stringify(selectedSext.element_configuration.magnetic_element.main_multipole_strength) : "No value"}</td>
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
          <Modal.Title>update Sextupoles</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Row className="mb-3">
            <Form.Group controlId="sextSelect_radios">
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
                    let index = sextupoles.findIndex((sext) => sext.name === formData.name);
                    let previousQuad = sextupoles[index - 1];
                    let nextQuad = sextupoles[index + 1];
                    console.log("current sext index is ", index);
                    console.log("previous sext is ", previousQuad);
                    console.log("next sext is ", nextQuad);

                    return (
                      <>
                        {previousQuad && (
                          <Form.Check
                            type="radio"
                            id="sext11"
                            name="sext"
                            label={`Previous sext (${previousQuad.name})`}
                            value={previousQuad.index}
                            checked={selected_drift_RadioOption === previousQuad.index.toString()}
                            onChange={(e) => setSelected_drift_RadioOption(e.target.value)}
                          />
                        )}

                        {nextQuad && (
                          <Form.Check
                            type="radio"
                            id="sext2"
                            name="sext"
                            label={`Next Sextupole (${nextQuad.name})`}
                            value={nextQuad.index}
                            checked={selected_drift_RadioOption === nextQuad.index.toString()}
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

                value={selectedSext ? formData.passMethod : ""}
                onChange={handleInputChange}
              />
            </Form.Group>

            <Form.Group as={Col} md="6" size="sm" controlId="tags">
              <Form.Label>Tags:</Form.Label>
              <Form.Control
                type="text"
                value={selectedSext ? formData.tags : ""}
                onChange={handleInputChange}
              />
            </Form.Group>

          </Row>


          <Row>

            <Form.Group as={Col} md="6" size="sm" controlId="updateLength">
              <Form.Label> Length:</Form.Label>
              <Form.Control
                type="number"

                value={selectedSext ? formData.updateLength : 0}
                onChange={handleInputChange}
              />
            </Form.Group>

            <Form.Group as={Col} md="6" size="sm" controlId="updateCorrector">
              <Form.Label>Correctors:</Form.Label>
              <Form.Control
                type="number"
                step="0.01"
                value={selectedSext ? formData.updateCorrector : ""}
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
                value={selectedSext ? formData.updateKickangleX : 0}
                onChange={handleInputChange}
              />
            </Form.Group>

            <Form.Group as={Col} md="6" controlId="updateKickangleY">
              <Form.Label> (Y):</Form.Label>
              <Form.Control
                type="number"
                step="0.01"
                value={selectedSext ? formData.updateKickangleY : 0}
                onChange={handleInputChange}
              />
            </Form.Group>
          </Row>
          <Row>
            <Form.Group as={Col} md="6" controlId="updatesnormal_coefficientsX">
              <Form.Label>Normal Coefficients (x) :</Form.Label>
              <Form.Control
                type="number"
                step="0.01"
                value={selectedSext ? formData.updatesnormal_coefficientsX : 0}
                onChange={handleInputChange}
              />
            </Form.Group>

            <Form.Group as={Col} md="6" controlId="updatenormal_coefficientsY">
              <Form.Label>  (y):</Form.Label>

              <Form.Control
                type="number"
                step="0.01"
                value={selectedSext ? formData.updatenormal_coefficientsY : 0}
                onChange={handleInputChange}
              />
            </Form.Group>

          </Row>

          <Row>
            <Form.Group as={Col} md="6" controlId="updateskew_coefficientsX">
              <Form.Label>Skew Coefficients (x):</Form.Label>
              <Form.Control
                type="number"
                step="0.01"
                value={selectedSext ? formData.updateskew_coefficientsX : 0}
                onChange={handleInputChange}
              />
            </Form.Group>

            <Form.Group as={Col} md="6" controlId="updateskew_coefficientsY">
              <Form.Label> (Y) :</Form.Label>

              <Form.Control
                type="number"
                step="0.01"
                value={selectedSext ? formData.updateskew_coefficientsY : 0}
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
                value={selectedSext ? formData.updateMainMultipoleIndex : 0}
                onChange={handleInputChange}
              />
            </Form.Group>

            <Form.Group as={Col} md="6" controlId="updateMainMultipoleStrenght">
              <Form.Label>main multiple strenght:</Form.Label>
              <Form.Control
                type="number"
                step="0.01"
                value={selectedSext ? formData.updateMainMultipoleStrenght : 0}
                onChange={handleInputChange}
              />
            </Form.Group>
          </Row>


        </Modal.Body>


        <Modal.Footer>
          <Button variant="secondary" onClick={toggleModal}>
            Close
          </Button>
          <Button variant="primary" onClick={handleUpdateSext}>
            Update
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
};

export default MyComponent;

