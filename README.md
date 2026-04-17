# Hacker News (ASW)

Monorepo del proyecto tipo **Hacker News** para *Aplicacions i Serveis Web* (ASW): **API REST (Django)** y **SPA (React + Vite)** en un solo repositorio.

| Parte | Ruta | Descripción |
|--------|------|-------------|
| **Backend** | [`backend/`](backend/) | Django, DRF, SQLite (local), S3 opcional, Swagger/ReDoc |
| **Frontend** | [`frontend/`](frontend/) | React, Vite, axios |

## Requisitos rápidos

- **Backend:** Python 3.11+, `pip`, `venv`.
- **Frontend:** Node.js 18+ y npm (ver [`frontend/README.md`](frontend/README.md)).

## Puesta en marcha

### API (desde la raíz del repo)

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

Más detalle: [**backend/README.md**](backend/README.md).

### Frontend

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

Configura `VITE_API_URL` y las claves de perfil en `.env.local`. Más detalle: [**frontend/README.md**](frontend/README.md).

## Estructura del repositorio

```text
.
├── README.md
├── backend/          # Proyecto Django (API + vistas HTML)
└── frontend/           # Proyecto React (Vite)
```
