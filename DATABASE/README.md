# FastAPI + SQLAlchemy Project Workflow

## Project Structure

```text
DATABASE/
│
├── database.py
├── model.py
├── create_table.py
├── project.py
└── .env
```

---

# 1. database.py

### Purpose
Responsible for database configuration and connection management.

### Responsibilities
- Load environment variables from `.env`
- Create SQLAlchemy Engine
- Create Session Factory
- Provide database session dependency (`getDB()`)
- Create Declarative Base (`Base`)

### Flow

```text
.env
  ↓
database.py
  ↓
Engine
  ↓
SessionLocal
  ↓
Base
```

---

# 2. model.py

### Purpose
Defines database tables using SQLAlchemy ORM models.

### Responsibilities
- Import `Base` from `database.py`
- Create table classes
- Define columns and datatypes

### Example Flow

```text
Base
  ↓
Book Model
  ↓
books Table
```

Example:

```python
class Book(Base):
    __tablename__ = "books"
```

---

# 3. create_table.py

### Purpose
Creates physical tables inside MySQL.

### Responsibilities
- Import all models
- Register models with Base metadata
- Execute table creation

### Flow

```text
Import Models
      ↓
Base.metadata
      ↓
create_all()
      ↓
Tables Created in MySQL
```

Code:

```python
Base.metadata.create_all(bind=engine)
```

---

# 4. project.py

### Purpose
Main FastAPI application.

### Responsibilities
- Define API endpoints
- Receive requests
- Validate data using Pydantic
- Interact with database through SQLAlchemy Session

### Flow

```text
Client Request
      ↓
FastAPI Route
      ↓
Pydantic Validation
      ↓
Database Session
      ↓
SQLAlchemy Model
      ↓
MySQL
```

---

# Complete Application Workflow

```text
          .env
            │
            ▼
      database.py
            │
            ├── Engine
            ├── SessionLocal
            └── Base
                    │
                    ▼
               model.py
                    │
                    ▼
            create_table.py
                    │
                    ▼
            MySQL Tables
                    │
                    ▼
              project.py
                    │
       ┌────────────┴────────────┐
       ▼                         ▼
   POST /books             GET /books
       │                         │
       ▼                         ▼
   Insert Record          Fetch Records
       │                         │
       └────────────┬────────────┘
                    ▼
                  MySQL
```

---

# Request Lifecycle

### Creating a Book

1. Client sends POST request.
2. FastAPI receives request.
3. Pydantic validates request body.
4. `getDB()` creates a Session.
5. SQLAlchemy creates a Book object.
6. `db.add()` stages record.
7. `db.commit()` saves record.
8. `db.refresh()` fetches latest values.
9. Response returned to client.
10. Session closed automatically.

---

# Key Concepts

## Engine
- Database connection manager.
- Knows how to connect to MySQL.

## Session
- Workspace between Python and Database.
- Handles CRUD operations and transactions.

## Base
- Parent class for ORM models.
- Tracks metadata of all tables.

## Model
- Python representation of a database table.

## Pydantic Schema
- Validates incoming API data.

---

# Summary

- `database.py` → Connection setup and session management.
- `model.py` → Database table definitions.
- `create_table.py` → Creates tables in MySQL.
- `project.py` → Exposes REST APIs and performs CRUD operations.

Together they form the complete FastAPI + SQLAlchemy workflow.
