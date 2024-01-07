window.onload = async function () {
  await loadStock();

  // Add an event listener to the search input
  const searchInput = document.getElementById("searchInput");
  searchInput.addEventListener("input", function () {
    const searchTerm = searchInput.value.toLowerCase();
    filterDataBySearchTerm(searchTerm);
  });

  // Add an event listener for the clear button
  const clearButton = document.getElementById("clearButton");
  clearButton.addEventListener("click", async function () {
    searchInput.value = ""; // Clear the input
    filterDataBySearchTerm(""); // Clear the filter
    await reloadTableData(); // Reload the table data
  });
};
async function reloadTableData() {
  const ucTable = document.querySelector("#uc-table-stock");
  ucTable.innerHTML = ""; // Clear the existing table

  await loadStock();
}
function filterDataBySearchTerm(searchTerm) {
  const ucTable = document.querySelector("#uc-table-stock");
  const rows = ucTable.querySelectorAll(".uc-table-row");

  rows.forEach((row) => {
    const nameCell = row.querySelector(".uc-table-row-data-name");
    const name = nameCell.textContent.toLowerCase().trim();

    if (name.includes(searchTerm)) {
      row.style.display = "uc-table-row"; // Show the row
    } else {
      row.style.display = "none"; // Hide the row
    }
  });
}
