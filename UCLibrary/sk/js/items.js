class book_data {
  constructor(Book_ID, Book_Name, Book_Status) {
    this.Book_ID = Book_ID
    this.Book_Name = Book_Name
    this.Book_Status = Book_Status
  }

  setId(id) {
    this.Book_ID = id
  }
  async isUnique(id) {
    // CHECK IF ITEM's ID IS UNIQUE
    return true
  }
  async save() {
    // SAVE TO DB
    return await fetch("http://localhost:5000/book_data", {
        method: "POST",
        body: JSON.stringify(this),
        headers: {
            "Content-Type": "application/json"
        }
    })
  }
  async update(book_id) {
    if (item_name) this.Book_Name = Book_Name
    if (item_type) this.Book_Status = Book_Status
    // UPDATE TO DB
    return await fetch(`http://localhost:5000/book_data/${this.book_id}`, {
        method: "PUT",
        body: JSON.stringify(this),
        headers: {
            "Content-Type": "application/json"
        }
    })
  }
async erase(item_id) {
    if (item_id) this.item_id = item_id;
    // ERASE DB
    return await fetch(`http://localhost:5000/item/${this.item_id}`, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
        }
    });
}
}

