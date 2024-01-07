class Borrow {
  constructor(BBook_ID, BName) {
    this.BBook_ID = BBook_ID;
    this.BName = BName;
  }

  async save() {
    // SAVE TO DB
    return await fetch("http://localhost:5000/borrow", {
        method: "POST",
        body: JSON.stringify(this),
        headers: {
            "Content-Type": "application/json"
        }
    });
  }
}