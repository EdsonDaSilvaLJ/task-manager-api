# Task Manager API

A REST API for managing tasks and projects, built with Django and Django REST Framework. This project demonstrates modern software engineering practices: JWT authentication, Docker containerization, automated testing, and a CI pipeline with GitHub Actions.

![CI Pipeline](https://github.com/edsondasilvalj/task-manager-api/actions/workflows/ci.yml/badge.svg)

---

## Tech Stack

| Layer | Technology |
|---|---|
| API | Django 6 + Django REST Framework |
| Authentication | JWT via Simple JWT |
| Database | PostgreSQL 16 |
| Server | Gunicorn + Nginx |
| Containerization | Docker + Docker Compose |
| Testing | Django Test + APIClient |
| CI | GitHub Actions |

---

## Architecture

```
internet → Nginx (port 80) → Gunicorn/Django (port 8000) → PostgreSQL (port 5432)
```

The project runs across 3 containers orchestrated by Docker Compose:

- **`database`** — PostgreSQL, data persisted in a volume
- **`django`** — Django application served by Gunicorn
- **`nginx`** — reverse proxy, serves static files directly

---

## Features

- User registration and authentication via email and password
- Login returning JWT tokens (access + refresh)
- Full CRUD for projects
- Full CRUD for tasks with priority, status, and due date fields
- Filtering by status and priority
- Full-text search on titles and descriptions
- Data isolation — each user can only access their own projects and tasks

---

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/your-username/task-manager-api.git
cd task-manager-api

# 2. Set up environment variables
cp api/.env.example api/.env
# edit api/.env with your values

# 3. Start the containers
docker compose up --build

# 4. The API will be available at http://localhost
```

### Create a superuser (optional)

```bash
docker compose exec django python manage.py createsuperuser
# admin panel available at http://localhost/admin
```

---

## Environment Variables

Create an `api/.env` file based on `api/.env.example`:

```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=taskdb
DB_USER=taskuser
DB_PASSWORD=taskpassword
DB_HOST=database
DB_PORT=5432
```

---

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth required |
|---|---|---|---|
| POST | `/api/accounts/register/` | Register a new user | No |
| POST | `/api/accounts/login/` | Login, returns JWT tokens | No |
| GET | `/api/accounts/me/` | Get current user data | Yes |
| PATCH | `/api/accounts/me/` | Update current user data | Yes |
| POST | `/api/accounts/token/refresh/` | Refresh access token | No |
| POST | `/api/accounts/token/blacklist/` | Logout, invalidates token | Yes |

### Projects

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/projects/` | List projects |
| POST | `/api/projects/` | Create a project |
| GET | `/api/projects/{id}/` | Retrieve project with tasks |
| PUT/PATCH | `/api/projects/{id}/` | Update project |
| DELETE | `/api/projects/{id}/` | Delete project |

### Tasks

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/tasks/` | List tasks |
| POST | `/api/tasks/` | Create a task |
| GET | `/api/tasks/{id}/` | Retrieve task |
| PUT/PATCH | `/api/tasks/{id}/` | Update task |
| DELETE | `/api/tasks/{id}/` | Delete task |

### Query Parameters

```
GET /api/tasks/?status=TODO
GET /api/tasks/?priority=H
GET /api/tasks/?project=1
GET /api/tasks/?search=bug
GET /api/tasks/?ordering=-created_at
```

---

## Usage Examples

### Register

```bash
curl -X POST http://localhost/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "name": "John Doe",
    "password1": "mypassword123",
    "password2": "mypassword123"
  }'
```

### Login

```bash
curl -X POST http://localhost/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "mypassword123"
  }'
```

Response:
```json
{
  "access": "eyJ...",
  "refresh": "eyJ..."
}
```

### Create a task

```bash
curl -X POST http://localhost/api/tasks/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "Write unit tests",
    "priority": "H",
    "status": "TODO",
    "project": 1
  }'
```

---

## Using as a Backend for Frontend Projects

This API is ready to be consumed by any frontend application (React, Vue, Next.js, etc.). Here's everything you need to get started.

### 1. Start the API

```bash
git clone https://github.com/your-username/task-manager-api.git
cd task-manager-api
cp api/.env.example api/.env
docker compose up --build
```

The API will be available at `http://localhost`.

### 2. Authentication flow

```js
// Register
const res = await fetch('http://localhost/api/accounts/register/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    name: 'John Doe',
    password1: 'mypassword123',
    password2: 'mypassword123',
  }),
});

// Login — store the tokens
const { access, refresh } = await fetch('http://localhost/api/accounts/login/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email: 'user@example.com', password: 'mypassword123' }),
}).then(r => r.json());

localStorage.setItem('access', access);
localStorage.setItem('refresh', refresh);
```

### 3. Authenticated requests

```js
const token = localStorage.getItem('access');

// fetch projects
const projects = await fetch('http://localhost/api/projects/', {
  headers: { 'Authorization': `Bearer ${token}` },
}).then(r => r.json());

// create a task
await fetch('http://localhost/api/tasks/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  },
  body: JSON.stringify({
    title: 'Build login page',
    priority: 'H',
    status: 'TODO',
    project: 1,
  }),
});
```

### 4. Refresh the access token

Access tokens expire after 30 minutes. Refresh them silently in the background:

```js
const { access } = await fetch('http://localhost/api/accounts/token/refresh/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ refresh: localStorage.getItem('refresh') }),
}).then(r => r.json());

localStorage.setItem('access', access);
```

### 5. Logout

```js
await fetch('http://localhost/api/accounts/token/blacklist/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem('access')}`,
  },
  body: JSON.stringify({ refresh: localStorage.getItem('refresh') }),
});

localStorage.removeItem('access');
localStorage.removeItem('refresh');
```

### CORS

If your frontend runs on a different port (e.g. `http://localhost:3000`), you'll need to enable CORS. Install and configure `django-cors-headers`:

```bash
pip install django-cors-headers
```

Add to `api/core/settings.py`:

```python
INSTALLED_APPS = [
    ...
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # must be before CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    ...
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',  # your frontend URL
]
```

---

## Running Tests

```bash
# run all tests
docker compose exec django python manage.py test --verbosity=2

# run tests for a specific app
docker compose exec django python manage.py test accounts
docker compose exec django python manage.py test tasks
```

The project includes 22 tests covering authentication, models, and data isolation between users.

---

## CI Pipeline

Every push to the `main` branch automatically:

1. Spins up a temporary PostgreSQL database
2. Installs all dependencies
3. Runs all 22 tests
4. Reports the result in the repository's Actions tab

The execution history is publicly visible on GitHub, demonstrating the codebase is always tested.

---

## Project Structure

```
task-manager-api/
├── .github/
│   └── workflows/
│       └── ci.yml          # test pipeline
├── api/
│   ├── core/               # Django settings
│   ├── accounts/           # authentication and users
│   │   ├── models.py       # Custom User Model (email-based login)
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── tests/
│   ├── tasks/              # projects and tasks
│   │   ├── models.py       # Project, Task with TextChoices
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── filters.py
│   │   └── tests/
│   ├── nginx/
│   │   └── nginx.conf
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── requirements.txt
│   └── .env.example
└── README.md
```

---

## Technical Decisions

**Custom User Model** — email-based login instead of username, created before the first migration to avoid painful refactoring later.

**JWT with blacklist** — invalidated tokens on logout are stored in the database, preventing reuse even before they expire.

**Queryset-level isolation** — each viewset filters data by the authenticated user in `get_queryset`, ensuring a user can never access another user's data even if they know the resource ID.

**Nginx as reverse proxy** — separates static file serving from Django, improving performance and security.

**Healthcheck in Compose** — the Django container only starts after PostgreSQL is ready to accept connections, preventing startup race conditions.
