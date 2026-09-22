# ToDo App — FastAPI Learning Project

A simple ToDo REST API built step by step while learning **FastAPI**, following an
industry-standard, feature-based project structure. This project is primarily a
learning exercise — the ToDo app itself is just a vehicle for practicing FastAPI,
Pydantic, and (soon) SQLAlchemy.

## Tech Stack

- **FastAPI** — web framework
- **Pydantic** — request/response data validation
- **Uvicorn** — ASGI server
- Data is currently stored **in-memory** (no database yet)

## Project Structure

```
src/
├── main.py                  # FastAPI app instance, router registration
└── features/
    └── todos/
        ├── router.py         # API endpoints (CRUD)
        └── schemas.py        # Pydantic models (TodoBase, TodoCreate, TodoResponse)
```

> The full target structure (feature-based modules, `db/`, `core/`, etc.) follows an
> industry-standard FastAPI layout and will be filled in gradually as new concepts
> are introduced.

## Features Implemented So Far

- `POST /todos/` — create a new todo
- `GET /todos/` — list all todos
- `GET /todos/{todo_id}` — get a single todo by id
- `PUT /todos/{todo_id}` — update a todo
- `DELETE /todos/{todo_id}` — delete a todo

Each todo has: `title`, `description` (optional), `priority`, `completed`, and an
auto-generated `id`.

## Running the Project

```bash
# install dependencies
pip install "fastapi[standard]"

# run the dev server
uvicorn src.main:app --reload
```

Then open:
- `http://127.0.0.1:8000/docs` — Swagger UI
- `http://127.0.0.1:8000/redoc` — ReDoc

## Testing

API requests are documented and testable via the included `.http` file
(PyCharm HTTP Client), covering all CRUD endpoints. Postman can also be used
against the same base URL.

## Roadmap

- [ ] Replace in-memory storage with **SQLAlchemy** models
- [ ] Add a real database (SQLite to start, PostgreSQL later)
- [ ] Repository / service layer separation
- [ ] Database migrations with Alembic

## Status

🚧 Work in progress — actively being built as part of a hands-on FastAPI learning path.
