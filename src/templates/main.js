document.addEventListener("DOMContentLoaded", function() {
  const submitBtn = document.querySelector("#submitBtn");
  const responseDiv = document.querySelector("#response");

  submitBtn.addEventListener("click", function() {
    const machineId = document.querySelector("#machineId").value;
    fetch(`/machine/${machineId}`)
      .then(function(response) {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error("Response not OK");
        }
      })
      .then(function(data) {
        let html = "";
        for (const [key, value] of Object.entries(data)) {
          html += `${key}: ${JSON.stringify(value)}<br>`;
        }
        responseDiv.innerHTML = html;
      })
      .catch(function(error) {
        console.error(error);
      });
  });
});
