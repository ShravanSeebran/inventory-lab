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
   git clone https://github.com/ShravanSeebran/inventory-lab.git
   cd inventory-lab
   ```

2. Install [uv](https://docs.astral.sh/uv/) and sync the locked dependencies (Python 3.13):

   ```bash
   cd backend
   uv sync --frozen
   ```

3. Run the server:

   ```bash
   uv run uvicorn app.main:app --reload
   ```

4. Open the registration page or API docs:

   * [Create account](http://127.0.0.1:8000/register)
   * [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

The frontend is served by FastAPI on the same origin; no frontend build is needed.
Tables are created on startup. By default, accounts persist in `backend/inventory.db`
when launched from `backend`. Set `DATABASE_URL` to use a different database.
Public registration accepts username, email, first name, last name, and password;
accounts are always created active and without administrator privileges.

### Tests

Run from `backend`:

```bash
uv run playwright install chromium
uv run pytest
```

The suite covers the API with isolated SQLite databases and submits the real
registration form in a headless browser. To use installed Microsoft Edge instead,
set `BROWSER_CHANNEL=msedge` before running pytest; the Chromium download is then
unnecessary. On machines with restricted temporary directories, pass pytest a
writable `--basetemp` directory reserved for tests.

---

### Team

* Kea 
* Shravan 
* Miguel 

---
