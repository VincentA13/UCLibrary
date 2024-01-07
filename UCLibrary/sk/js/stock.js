window.onload = async function() {
  await loadStock();
}

async function loadStock() {
  const response = await fetch("http://localhost:5000/book_data/", {
    method: "GET",
    headers: {
      "Content-Type": "application/json"
    }
  })

  if (response.status === 200) {
    const ucTable = document.querySelector("#uc-table-stock")
    const datas = await response.json()

    if (ucTable) {
      let inner = ""
      for (const data of datas) {
        const borrowStatus = data.BookStatus;

        // Check if BookStatus is 'Borrowed' and apply background color to the cell
        const statusStyle = borrowStatus === 'Borrowed' ? 'background-color: lightcoral;' : '';

        const template = `
          <div class="uc-table-row">
            <span class="uc-table-row-data uc-table-row-data-id">${data.BookID}</span>
            <span class="uc-table-row-data uc-table-row-data-name">${data.BookName}</span>
            <span class="uc-table-row-data uc-table-row-data-type" style="${statusStyle}">${borrowStatus}</span>
          </div>
        `;

        inner += template;
      }
      ucTable.innerHTML = inner;
    }
  }
}
