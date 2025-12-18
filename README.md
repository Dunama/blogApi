
# Social Book (Django)

A Django + Django REST Framework project that provides:

- A REST API (JWT auth) for posts, likes, and comments
- A session-based web UI (templates) for feed/profile interactions

## Tech Stack

- Python / Django
- Django REST Framework (DRF)
- SimpleJWT (JWT auth)
- SQLite (local default) or PostgreSQL via `DATABASE_URL` (Render)
- WhiteNoise (static files in production)
- Gunicorn (production WSGI server)
- Docker / Docker Compose (local container workflow)

## Run Locally (without Docker)

From the repo root:

1) Create/activate a virtual environment

- PowerShell:
	- `py -m venv .venv`
	- `. .venv\Scripts\Activate.ps1`

2) Install dependencies

- `pip install -r requirements.txt`

3) Run migrations

- `cd blog_api`
- `py manage.py migrate`

4) (Optional) Seed demo users

- `py manage.py seed_dummy_users`

5) Start the server

- `py manage.py runserver`

Open:

- Web UI: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`
- API base: `http://127.0.0.1:8000/api/`

## Run Locally (Docker)

Prerequisite: Docker Desktop running.

From the repo root (where `docker-compose.yaml` lives):

- `docker compose up --build`

If you get a Windows bind-mount error for SQLite, create the file once:

- `New-Item -ItemType File -Force "blog_api\db.sqlite3" | Out-Null`

## API (Postman Quick Test)

Base URL (local): `http://127.0.0.1:8000`

Auth:

- `POST /api/auth/signup/`
- `POST /api/auth/login/`
- `POST /api/auth/refresh/`
- `GET  /api/auth/me/`

Posts:

- `GET    /api/posts/` (paginated)
- `POST   /api/posts/` (auth)
- `GET    /api/posts/{id}/`
- `PATCH  /api/posts/{id}/` (author)
- `DELETE /api/posts/{id}/` (author)
- `POST   /api/posts/{id}/like/` (auth)

Comments:

- `GET    /api/comments/`
- `POST   /api/comments/` (auth)
- `GET    /api/comments/{id}/`
- `PATCH  /api/comments/{id}/` (author)
- `DELETE /api/comments/{id}/` (author)

## Extra Features Added

- Session-based web pages (templates): sign-in/sign-up/feed/profile/settings
- Feed interactions in web UI:
	- Create post
	- Like/unlike
	- Comment
	- Delete post (author-only)
- Follow/unfollow system with suggested users
- Management command to seed demo users: `seed_dummy_users`
- Pagination for API post listing (DRF PageNumberPagination)
- CI pipeline with GitHub Actions (runs checks, migrations, tests)

## Deployment (Render)

This repo includes `render.yaml`.

Required env vars on Render:

- `DJANGO_SECRET_KEY` (Render can generate)
- `DJANGO_DEBUG=0`
- `DJANGO_ALLOWED_HOSTS=.onrender.com,localhost,127.0.0.1`
- `DATABASE_URL` (if using Render Postgres)

Render build/start is configured to:

- Install dependencies
- Run `collectstatic`
- Run `migrate`
- Start Gunicorn

