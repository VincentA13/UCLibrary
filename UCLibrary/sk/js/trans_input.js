const button = document.querySelector("button.uc-form-button-submit");
let edit_item = null;

button.addEventListener("click", (e) => {
    e.preventDefault();

    const BBook_ID = document.querySelector("#BBook_ID").value;
    const BName = document.querySelector("#BName").value;

    if (BBook_ID && BName) {
        const borrow = new Borrow(BBook_ID, BName);
        borrow.save();
        setTimeout(() => {

        }, 1000);
    }
});

document.addEventListener('DOMContentLoaded', async function() {
    const edit_id = localStorage.getItem('item-edit-id');
    if (edit_id) {
        edit_item = await loadItem(edit_id);

        if (edit_item) {
            document.querySelector("#BBook_ID").value = edit_item.BookID || "";
            document.querySelector("#BookName").value = edit_item.BookName || "";
        }
    }
    localStorage.removeItem('item-edit-id');
});

async function loadItem(id) {
    try {
        const response = await fetch(`http://localhost:5000/book_data/${id}`, {
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
