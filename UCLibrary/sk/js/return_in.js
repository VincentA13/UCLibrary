class Return {
  constructor(Borrow_ID) {
    this.Borrow_ID = Borrow_ID;
  }

  async update() {
    return await fetch("http://localhost:5000/return", {
        method: "PUT",
        body: JSON.stringify(this),
        headers: {
            "Content-Type": "application/json"
        }
    });
  }
}