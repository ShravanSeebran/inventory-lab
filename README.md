# inventory-lab

##  Inventory Lab

A minimal inventory management system built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL** (or SQLite for now), designed to help us learn and test tech/tools for a larger logistics system.

---

###  Features

* Basic product model with create, read, update, delete (CRUD)
* REST API using FastAPI
* Modular codebase (models, schemas, routes)
* SQLite database (PostgreSQL planned)
* Organized project structure
* Sprint-based task management via GitHub Projects

---

###  Project Structure

```
inventory-lab/
├── app/
│   ├── main.py
│   ├── models/
│   ├── routes/
│   └── schemas/
├── requirements.txt
├── README.md
```

---

###  Sprint 1 Goals

*  Set up FastAPI starter app
*  Create basic folder structure
*  Build product model, schema, and routes
*  Set up database connection with SQLAlchemy
*  Run the app locally with Uvicorn

---

### Technologies

* FastAPI
* SQLAlchemy
* Pydantic
* Uvicorn
* SQLite (temporary)
* PostgreSQL (planned)
* GitHub Projects + Issues (for Agile-style tracking)

---

### How to Run Locally

1. Clone the repo:

   ```bash
   git clone https://github.com/shravan123/inventory-lab.git
   cd inventory-lab
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the server:

   ```bash
   uvicorn app.main:app --reload
   ```

4. Visit the docs:

   * [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### Team

* Kea 
* Shravan 
* Miguel 

---
