import axios from 'axios';
const baseurl='http://127.0.0.1:8000'
export const fetchMachines = async () => {

  try {
    const response = await axios.get(`/machine/machine`);
    console.log("response:", response.data)
    return response.data;
  } catch (error) {
    console.error('Error fetching machines:', error);
    throw error;
  }
};

// get all quads
export const fetchQuadrupoles = async (machineId) => {
  try {
    const response = await axios.get(`/machine/machine/${machineId}/quad`);
    return response.data;
  } catch (error) {
    console.error('Error fetching quadrupoles:', error);
    throw error;
  }
};

//get all sextupoles
export const fetchSextupoles = async (machineId) => {
  try {
    const response = await axios.get(`/machine/machine/${machineId}/sextupole`);
    return response.data;
  } catch (error) {
    console.error('Error fetching sextupoles:', error);
    throw error;
  }
};

export const updateQuadrupole = async (machineId, quadName, affected_quad, formData,option_with_copy) => {
  try {
    
    const normalCoefficients = typeof formData.updatesnormal_coefficients === 'string' ? formData.updatesnormal_coefficients.split(',').map(parseFloat) : [];
    const skewCoefficients = typeof formData.updateskew_coefficients === 'string' ? formData.updateskew_coefficients.split(',').map(parseFloat) : [];

    const updated_data = {
      "type":"Quadrupole",
      "index": formData.index,
      "name": formData.name,

      "passmethod":formData.passMethod,
      "tags": [formData.tags],
      "length": formData.updateLength,
      "element_configuration": {
        "correctors": formData.updateCorrector==""?[]:formData.updateCorrector,
        "kickangle": { "x": formData.updateKickangleX, "y": formData.updateKickangleY },
        "magnetic_element": {
          "main_multipole_index": formData.updateMainMultipoleIndex,
          "main_multipole_strength": formData.updateMainMultipoleStrenght,
          "coeffs": {
            "normal_coefficients": normalCoefficients,
            "skew_coefficients": skewCoefficients
          }
        }
      }
    };
    console.log("updated object for submission is ",updated_data)

    let response;
    if (option_with_copy === 0) {
      response = await axios.put(`/machine/machine/${machineId}/quad/${quadName}`, {
        affected_drift: affected_quad === "" ? "-1" : affected_quad,
        updated_data: updated_data
      });
    } else {
      response = await axios.put(`/machine/machine/${machineId}/quad_copy/${quadName}`, {
        affected_drift: affected_quad === "" ? "-1" : affected_quad,
        updated_data: updated_data
      });
    }

    return response.data;

  } catch (error) {
    console.error('Error updating quadrupole:', error);
    throw error;
  }
};



//update sextu
export const updateSextupole = async (machineId, SextName, affected_sext, formData,option_with_copy) => {
  try {
    const normalCoefficients = typeof formData.updatesnormal_coefficients === 'string' ? formData.updatesnormal_coefficients.split(',').map(parseFloat) : [];
    const skewCoefficients = typeof formData.updateskew_coefficients === 'string' ? formData.updateskew_coefficients.split(',').map(parseFloat) : [];

    console.log("the value of the form data from the api to call", affected_sext, formData)
    const updated_data = {
      "type":"Sextupole",
      "index": formData.index,
      "name": formData.name,

      "passmethod":formData.passMethod,
      "tags": [formData.tags],
      "length": formData.updateLength,
      "element_configuration": {
        "correctors": formData.updateCorrector==""?[]:formData.updateCorrector,
        "kickangle": { "x": formData.updateKickangleX, "y": formData.updateKickangleY },
        "magnetic_element": {
          "main_multipole_index": formData.updateMainMultipoleIndex,
          "main_multipole_strength": formData.updateMainMultipoleStrenght,
          "coeffs": {
            "normal_coefficients": normalCoefficients,
            "skew_coefficients": skewCoefficients
          }
        }
      }
    };
    console.log("updated object for submission is ",updated_data)
    let response;
    if (option_with_copy === 0) {
     response = await axios.put(`/machine/machine/${machineId}/sext/${SextName}`,
      {
        affected_drift: affected_sext === "" ? "-1" : affected_sext,
        updated_data: updated_data
      });
    }
    else {

      response = await axios.put(`/machine/machine/${machineId}/sext_copy/${SextName}`,
      {
        affected_drift: affected_sext === "" ? "-1" : affected_sext,
        updated_data: updated_data
      });

    }
    return response.data;
  } catch (error) {
    console.error('Error updating sextupole:', error);
    throw error;
  }
};


//get all drifts
export const fetchDrifts = async (machineId) => {
  try {
    const response = await axios.get(`/machine/machine/${machineId}/drifts`);
    return response.data;
  } catch (error) {
    console.error('Error fetching drifts:', error);
    throw error;
  }
};

//update drifts
export const updateDrifts = async (machineId, DriftName, affected_drift, formData) => {
  try {
    console.log("the value of the form data from the api to call", affected_drift, formData)
    const updated_data = {
      "type":"Drift",
      "index": formData.index,
      "name": formData.name,

      "passmethod":formData.passMethod,
      "tags": [formData.tags],
      "length": formData.updateLength
    };
    console.log("updated object for submission is ",updated_data)
    const response = await axios.put(`/machine/machine/${machineId}/drift/${DriftName}`,
    {
      affected_drift: affected_drift === "" ? "-1" : affected_drift,
      updated_data: updated_data
    });
    return response.data;
  } catch (error) {
    console.error('Error updating drift:', error);
    throw error;
  }
};

//get all markers
export const fetchMarkers = async (machineId) => {
  try {
    const response = await axios.get(`/machine/machine/${machineId}/markers`);
    return response.data;
  } catch (error) {
    console.error('Error fetching markers:', error);
    throw error;
  }
};

//update marker
export const updateMarkers = async (machineId, MarkerName, affected_marker, formData) => {
  try {
    console.log("the value of the form data from the api to call", affected_marker, formData)
    const updated_data = {
      "type":"Marker",
      "index": formData.index,
      "name": formData.name,

      "passmethod":formData.passMethod,
      "tags": [formData.tags],
      "length": formData.updateLength
    };
    console.log("updated object for submission is ",updated_data)
    const response = await axios.put(`/machine/machine/${machineId}/marker/${MarkerName}`,
    {
      affected_marker: affected_marker === "" ? "-1" : affected_marker,
      updated_data: updated_data
    });
    return response.data;
  } catch (error) {
    console.error('Error updating marker:', error);
    throw error;
  }
};


//get all monitor
export const fetchMonitor = async (machineId) => {
  try {
    const response = await axios.get(`/machine/machine/${machineId}/monitors`);
    return response.data;
  } catch (error) {
    console.error('Error fetching monitors:', error);
    throw error;
  }
};

//update monitor
export const updateMonitors = async (machineId, MonitorName, affected_monitor, formData) => {
  try {
    console.log("the value of the form data from the api to call", affected_monitor, formData)
    const updated_data = {
      "type":"Monitor",
      "index": formData.index,
      "name": formData.name,

      "passmethod":formData.passMethod,
      "tags": [formData.tags],
      "length": formData.updateLength
    };
    console.log("updated object for submission is ",updated_data)
    const response = await axios.put(`/machine/machine/${machineId}/monitor/${MonitorName}`,
    {
      affected_monitor: affected_monitor === "" ? "-1" : affected_monitor,
      updated_data: updated_data
    });
    return response.data;
  } catch (error) {
    console.error('Error updating monitor:', error);
    throw error;
  }
};



export const get_quad_from_seq = async (machineId, quadName, updatedData) => {
  try {
    const response = await axios.put(`/machine/${machineId}/quad/${quadName}`, updatedData);
    return response.data;
  } catch (error) {
    console.error('Error updating quadrupole:', error);
    throw error;
  }
};

