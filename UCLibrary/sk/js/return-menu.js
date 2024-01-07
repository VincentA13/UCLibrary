window.onload = async function() {
  await loadStock()
}

async function loadStock() {
  const response = await fetch("http://localhost:5000/book_return/", {
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
        const template = `
          <div class="uc-table-row" onclick="clickHandler('${data.Borrow_ID}')">
            <span class="uc-table-row-data uc-table-row-data-id">${data.Borrow_ID}</span>
            <span class="uc-table-row-data uc-table-row-data-name">${data.BName}</span>
            <span class="uc-table-row-data uc-table-row-data-type">${data.FormattedRDate}</span>
          </div>
        `
        inner += template
      }
      ucTable.innerHTML = inner
    }
  }
}

function clickHandler(id) {
  localStorage.setItem('item-edit-id', id)
  window.location.href = './returnbook.html'
}