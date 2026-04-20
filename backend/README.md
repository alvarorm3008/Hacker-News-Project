# Hacker News — Backend API

REST API and server application for the **Hacker News-style** clone: stories, submissions, comments, threads, votes, and accounts. API prefix: **`/api/`**.

This code lives in the monorepo under **`backend/`**. From the repository root, enter this folder before running `manage.py`.

Main stack: **Django 5.x**, **Django REST Framework**, **django-cors-headers**, **django-allauth** (optional Google login), **drf-yasg** (OpenAPI), and optional **S3** storage via `django-storages`. In local mode, if AWS variables are not defined, local static/media folders are used.

---

## Contents

- [Requirements](#requirements)
- [Local Setup](#local-setup)
- [Environment Variables](#environment-variables)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)

---

## Requirements

| Environment | Recommended Version |
|-------------|---------------------|
| Python | 3.11+ |
| pip / venv | Included with Python |

---

## Local Setup

1. From the monorepo root:

   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Create `.env` from `.env.example` and fill in the required values (OAuth, AWS, etc. only if you use them).

3. Run migrations and start the server:

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

- API: http://127.0.0.1:8000/api/
- Swagger: http://127.0.0.1:8000/swagger/
- ReDoc: http://127.0.0.1:8000/redoc/

---

## Environment Variables

The **`backend/.env`** file (not versioned) is loaded automatically. Variable names and descriptions are in **`.env.example`**.

It includes, among others: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`, **Google OAuth** credentials (`GOOGLE_OAUTH_*`), and optional **AWS** variables for S3.

---

## API Documentation

Interactive docs powered by **drf-yasg** are available at **`/swagger/`** and **`/redoc/`**. There is also an **`api.yaml`** file in this folder as reference.

The REST API uses **API key** authentication through the `Authorization` header (see the `accounts` app and `REST_FRAMEWORK` config in `ASWproject/settings.py`).

---

## Project Structure

| Path / app | Role |
|------------|------|
| `ASWproject/` | Settings and root URLs |
| `api/` | REST routes under `/api/` |
| `news/`, `newest/`, `ask/` | Listings and related views |
| `submissions/`, `comments/`, `threads/` | Submissions, comments, threads |
| `accounts/` | Profiles, karma, API keys, allauth |
