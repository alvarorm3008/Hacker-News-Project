# Hacker News (ASW)

Monorepo for a **Hacker News-style** project built for *Aplicacions i Serveis Web* (ASW): **REST API (Django)** and **SPA (React + Vite)** in a single repository.

| Part | Path | Description |
|------|------|-------------|
| **Backend** | [`backend/`](backend/) | Django, DRF, local SQLite, optional S3, Swagger/ReDoc |
| **Frontend** | [`frontend/`](frontend/) | React, Vite, axios |

## Quick Requirements

- **Backend:** Python 3.11+, `pip`, `venv`.
- **Frontend:** Node.js 18+ and npm (see [`frontend/README.md`](frontend/README.md)).

## Getting Started

### API (from repository root)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

Swagger: http://127.0.0.1:8000/swagger/

More details: [**backend/README.md**](backend/README.md).

### Frontend

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

Set `VITE_API_URL` and profile keys in `.env.local`. More details: [**frontend/README.md**](frontend/README.md).

## Repository Structure

```text
.
├── README.md
├── backend/            # Django project (API + HTML views)
└── frontend/           # React project (Vite)
```
