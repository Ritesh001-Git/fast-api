# FastAPI Authentication Project

## Overview

This project implements a complete authentication and authorization system using:

- FastAPI
- SQLAlchemy ORM
- MySQL
- JWT (JSON Web Tokens)
- Passlib (Argon2 password hashing)
- OAuth2 Password Flow

The application allows users to:

1. Register (`/signup`)
2. Login (`/login`)
3. Receive a JWT access token
4. Access protected routes
5. Access role-based routes (User/Admin)

---

# Project Structure

```text
AUTH/
│
├── main.py
├── auth_database.py
├── auth_table.py
├── model.py
├── schemas.py
├── utils.py
├── .env
└── requirements.txt
```

---

# Workflow Diagram

```text
User
 │
 ├── POST /signup
 │       │
 │       ▼
 │   schemas.py
 │       │
 │       ▼
 │   utils.py (hash password)
 │       │
 │       ▼
 │   model.py
 │       │
 │       ▼
 │   MySQL Database
 │
 └── POST /login
         │
         ▼
      model.py
         │
         ▼
      utils.py (verify password)
         │
         ▼
      JWT Token Generated
         │
         ▼
      Protected Routes
```

---

# auth_database.py

## Purpose

Creates the database connection and session management.

## Responsibilities

- Load environment variables
- Build MySQL connection string
- Create SQLAlchemy engine
- Create session factory
- Provide database dependency to FastAPI
- Define Base class for models

## Main Components

### Load Environment Variables

```python
load_dotenv()
```

Reads values from `.env`.

### Create Engine

```python
engine = create_engine(DATABASE_URL)
```

The engine is SQLAlchemy's connection to MySQL.

### SessionLocal

```python
SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)
```

Creates database sessions.

### getDB()

```python
def getDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Used by FastAPI dependency injection.

---

# model.py

## Purpose

Defines database tables using SQLAlchemy ORM.

## User Model

```python
class User(Base):
```

Represents a user record in the database.

### Columns

| Column | Purpose |
|----------|----------|
| id | Primary key |
| username | Unique username |
| email | User email |
| hashed_password | Encrypted password |
| role | user/admin role |

### Example Record

```text
id: 1
username: ritesh
email: ritesh@gmail.com
hashed_password: $argon2id...
role: admin
```

---

# auth_table.py

## Purpose

Creates database tables.

### Code

```python
Base.metadata.create_all(bind=engine)
```

What happens:

1. Reads all models
2. Checks database
3. Creates missing tables

Run:

```bash
python auth_table.py
```

---

# schemas.py

## Purpose

Defines request/response validation using Pydantic.

Schemas validate incoming API data before it reaches business logic.

## UserCreate

```python
class UserCreate(BaseModel):
```

Used by:

```http
POST /signup
```

Expected data:

```json
{
  "username":"ritesh",
  "email":"ritesh@gmail.com",
  "password":"secret123",
  "role":"user"
}
```

## UserLogin

```python
class UserLogin(BaseModel):
```

Used for login data validation.

---

# utils.py

## Purpose

Contains password utilities.

## Password Hashing

```python
hash_password()
```

Converts:

```text
secret123
```

into:

```text
$argon2id$v=19$...
```

before saving to the database.

## Password Verification

```python
verify_password()
```

Checks:

```text
User Input Password
```
against

```text
Stored Hashed Password
```

without exposing the original password.

---

# main.py

## Purpose

Main FastAPI application.

Contains:

- API routes
- JWT logic
- Authentication
- Authorization
- Dependency injection

---

## create_access_token()

Creates JWT token.

```python
jwt.encode(...)
```

Payload example:

```json
{
  "sub":"ritesh",
  "role":"admin",
  "exp":"2026-01-01"
}
```

---

## /signup Route

### Flow

```text
User
 │
 ▼
Request Body Validation
 │
 ▼
Check Existing User
 │
 ▼
Hash Password
 │
 ▼
Save User
 │
 ▼
Return Response
```

---

## /login Route

### Flow

```text
User
 │
 ▼
Find Username
 │
 ▼
Verify Password
 │
 ▼
Generate JWT
 │
 ▼
Return Access Token
```

Example response:

```json
{
  "access_token":"eyJhbGciOiJIUzI1NiIs...",
  "token_type":"bearer"
}
```

---

## OAuth2PasswordBearer

```python
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)
```

Extracts JWT token from:

```http
Authorization: Bearer TOKEN
```

---

## get_current_user()

### Responsibilities

1. Read JWT
2. Decode JWT
3. Validate token
4. Extract username and role

Returns:

```python
{
    "username":"ritesh",
    "role":"admin"
}
```

---

# Protected Routes

## /protected

Requires valid JWT.

```text
Login
 │
 ▼
Get Token
 │
 ▼
Pass Token
 │
 ▼
Access Route
```

---

# Role-Based Access Control

## require_roles()

Checks user role.

Example:

```python
require_roles(["admin"])
```

Only admin users can access the route.

---

## User Dashboard

```python
/user/dashboard
```

Allowed:

```text
user
```

---

## Admin Dashboard

```python
/admin/dashboard
```

Allowed:

```text
admin
```

---

# Environment Variables

Example `.env`

```env
MYSQL_USER=root
MYSQL_PASSWORD=password
MYSQL_DB=fastapi_db
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306

SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

# Complete Authentication Flow

```text
REGISTER
========
User
 │
 ▼
POST /signup
 │
 ▼
Validate Schema
 │
 ▼
Hash Password
 │
 ▼
Store in MySQL

LOGIN
=====
User
 │
 ▼
POST /login
 │
 ▼
Verify Password
 │
 ▼
Generate JWT
 │
 ▼
Return Token

AUTHORIZATION
=============
User
 │
 ▼
Authorization: Bearer TOKEN
 │
 ▼
Decode JWT
 │
 ▼
Check Role
 │
 ▼
Allow / Deny Access
```

---

# Technologies Used

- FastAPI
- SQLAlchemy
- MySQL
- PyMySQL
- Passlib
- Argon2
- Python-JOSE
- OAuth2
- Pydantic
- Uvicorn

---

# Author

Authentication API built with FastAPI, JWT, SQLAlchemy, and MySQL.
