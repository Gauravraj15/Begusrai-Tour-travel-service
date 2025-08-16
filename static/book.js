
    const fromSelect = document.getElementById("from_location");
    const customFromInput = document.getElementById("custom_from");

    const toSelect = document.getElementById("to_location");
    const customToInput = document.getElementById("custom_to");

    fromSelect.addEventListener("change", function () {
        if (this.value === "Custom") {
            customFromInput.style.display = "inline-block";
        } else {
            customFromInput.style.display = "none";
        }
    });

    toSelect.addEventListener("change", function () {
        if (this.value === "Custom") {
            customToInput.style.display = "inline-block";
        } else {
            customToInput.style.display = "none";
        }
    });

    function toggleCustomInput(selectId, inputId) {
      const select = document.getElementById(selectId);
      const input = document.getElementById(inputId);
      if (select.value === "Custom") {
        input.style.display = "block";
      } else {
        input.style.display = "none";
        input.value = ""; // clear previous value
      }
    }