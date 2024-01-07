window.onload = async function () {
  await loadStock();
  addEventHandlers();
};

function addEventHandlers() {
  // Add an event listener to the dropdown
  const transTypeFilter = document.getElementById("transTypeFilter");

  transTypeFilter.addEventListener("change", function () {
    // Get the selected value from the dropdown
    const selectedType = transTypeFilter.value;

    // Filter the table based on the selected value
    filterTable(selectedType);
  });
}

function filterTable(selectedType) {
  const ucTable = document.querySelector("#uc-table-stock");
  const rows = ucTable.querySelectorAll(".uc-table-row");

  rows.forEach((row) => {
    const typeCell = row.querySelector(".uc-table-row-data-ttype");
    const type = typeCell.textContent.trim(); // Trim whitespace from the type

    if (selectedType === "" || type === selectedType) {
      row.style.display = "flex"; // Show the row
    } else {
      row.style.display = "none"; // Hide the row
    }
  });
}