# 🚀 Project Tracker API

<p align="center">
  <strong>A modern, production-inspired backend for managing projects and tickets.</strong>
  <br>
  Built with <strong>FastAPI</strong>, <strong>PostgreSQL</strong>, <strong>Async SQLAlchemy</strong>, <strong>Alembic</strong>, and <strong>JWT Authentication</strong>.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white">
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white">
  <img src="https://img.shields.io/badge/SQLAlchemy-CC2927?style=for-the-badge">
  <img src="https://img.shields.io/badge/Alembic-222222?style=for-the-badge">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white">
  <img src="https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white">
</p>

---

## ✨ Features

- 🔐 JWT Authentication
- 👤 User Registration & Login
- 📁 Project CRUD with owner-only authorization
- 🎫 Ticket Management
- 🔍 Filter tickets by status, priority, assignee, and project
- 📝 Automatic Ticket History tracking
- ⚡ Async SQLAlchemy 2.0
- 📦 Alembic database migrations
- 🐳 Docker support
- 🧪 Async integration tests with Pytest
- 📖 Interactive Swagger & ReDoc documentation

---

# 📸 Demo

<p align="center">
    <img src="demo/test.png" width="900">
</p>

---

# 🏗️ Architecture

```text
                    Browser Demo / API Client
                              │
                     FastAPI Routers (/api/v1)
                              │
                      Service Layer
                (Business Logic & Validation)
                              │
                     Repository Layer
                     (Database Operations)
                              │
                Async SQLAlchemy ORM (2.0)
                              │
                        PostgreSQL Database
                              ▲
                    Pydantic Schemas
          (Validation, Serialization & Responses)
```

### Request Flow

```text
Client
   │
   ▼
FastAPI Router
   │
JWT Authentication
   │
Service Layer
   │
Repository Layer
   │
PostgreSQL
```

---

# 📂 Project Structure

```text
.
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   ├── static/
│   └── main.py
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── tests/
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# ⚙️ Local Development

### Requirements

- Python 3.11+
- PostgreSQL
- Virtual Environment

Clone the repository

```bash
git clone https://github.com/yourusername/project-tracker-api.git

cd project-tracker-api
```

Create environment variables

```bash
cp .env.example .env
```

Edit the database URL if necessary.

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows**

```powershell
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run database migrations

```bash
alembic upgrade head
```

Start the development server

```bash
uvicorn app.main:app --reload
```

---

# 🐳 Docker

Start everything with one command

```bash
cp .env.example .env

docker-compose up --build
```

This launches:

- FastAPI
- PostgreSQL
- Automatic Alembic migrations
- Health checks

Application:

```
http://localhost:8000
```

Swagger:

```
http://localhost:8000/docs
```

ReDoc:

```
http://localhost:8000/redoc
```

---

# 🗄️ Database Migrations

Apply migrations

```bash
alembic upgrade head
```

Generate a new migration

```bash
alembic revision --autogenerate -m "describe change"
```

Apply it

```bash
alembic upgrade head
```

---

# 🧪 Testing

Run all tests

```bash
pytest
```

Tests include:

- ✅ Authentication
- ✅ Project CRUD
- ✅ Permission checks
- ✅ Ticket CRUD
- ✅ Ticket filtering
- ✅ Automatic history tracking

SQLite is used during testing with an isolated database.

---

# 🚀 Example API Usage

## Register

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
-H "Content-Type: application/json" \
-d '{
  "email":"sam@example.com",
  "password":"password123",
  "full_name":"Sam Example"
}'
```

---

## Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
-H "Content-Type: application/json" \
-d '{
  "email":"sam@example.com",
  "password":"password123"
}'
```

---

## Create Project

```bash
curl -X POST http://localhost:8000/api/v1/projects \
-H "Authorization: Bearer $TOKEN" \
-H "Content-Type: application/json" \
-d '{
  "name":"Website Refresh",
  "description":"Q3 Development"
}'
```

---

## Create Ticket

```bash
curl -X POST http://localhost:8000/api/v1/projects/$PROJECT_ID/tickets \
-H "Authorization: Bearer $TOKEN" \
-H "Content-Type: application/json" \
-d '{
  "title":"Implement Login",
  "priority":"high"
}'
```

---

## Update Ticket

```bash
curl -X PATCH http://localhost:8000/api/v1/tickets/1 \
-H "Authorization: Bearer $TOKEN" \
-H "Content-Type: application/json" \
-d '{
  "status":"in_progress"
}'
```

---

# 🔒 Authentication

All protected endpoints require a Bearer JWT.

```http
Authorization: Bearer <your_access_token>
```

Project ownership is enforced so that only the owner can modify or delete a project.

Ticket updates automatically generate audit history records whenever:

- Status changes
- Priority changes
- Assignee changes

---

# 💻 Tech Stack

| Category | Technology |
|-----------|------------|
| Backend | FastAPI |
| Database | PostgreSQL |
| ORM | Async SQLAlchemy 2.0 |
| Validation | Pydantic |
| Authentication | JWT |
| Migrations | Alembic |
| Testing | Pytest |
| Containerization | Docker |

---

# 🌟 Future Improvements

- Email notifications
- Comments on tickets
- File attachments
- Team workspaces
- Role-based permissions (RBAC)
- WebSocket real-time updates
- CI/CD with GitHub Actions

---

## ⭐ If you found this project useful, consider giving it a star!
