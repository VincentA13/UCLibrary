const button = document.querySelector("button.uc-form-button-submit");
let edit_item = null;

button.addEventListener("click", (e) => {
    e.preventDefault();

    const Borrow_ID = document.querySelector("#Borrow_ID").value;

    if (Borrow_ID) {
        const retur = new Return(Borrow_ID);
        retur.update();
        setTimeout(() => {
            window.location.href = "Database-Stok-Search.html";
        }, 1000);
    }
});

document.addEventListener('DOMContentLoaded', async function() {
    const edit_id = localStorage.getItem('item-edit-id');
    if (edit_id) {
        edit_item = await loadItem(edit_id);

        if (edit_item) {
            document.querySelector("#Borrow_ID").value = edit_item.Borrow_ID || "";
            document.querySelector("#BName").value = edit_item.BName || "";
            document.querySelector("#RDate").value = edit_item.RDate || "";
        }
    }
    localStorage.removeItem('item-edit-id');
});

async function loadItem(id) {
    try {
        const response = await fetch(`http://localhost:5000/borrow/${id}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        });
        if (response.status === 200) {
            return await response.json();
        }
        return null;
    } catch {
        return null;
    }
}
