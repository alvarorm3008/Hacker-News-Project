# Hacker News — Backend API

API REST y aplicación servidor del clon tipo **Hacker News**: noticias, envíos, comentarios, hilos, votos y cuentas. El prefijo de la API es **`/api/`**.

Este código vive en el monorepo bajo la carpeta **`backend/`**. Desde la raíz del repositorio, entra aquí antes de ejecutar `manage.py`.

Stack principal: **Django 5.x**, **Django REST Framework**, **django-cors-headers**, **django-allauth** (Google opcional), **drf-yasg** (OpenAPI), almacenamiento en **S3** opcional vía `django-storages`; en local, sin variables AWS, se usan carpetas locales para estáticos y media.

---

## Contenido

- [Requisitos](#requisitos)
- [Puesta en marcha en local](#puesta-en-marcha-en-local)
- [Variables de entorno](#variables-de-entorno)
- [Documentación de la API](#documentación-de-la-api)
- [Estructura del proyecto](#estructura-del-proyecto)

---

## Requisitos

| Entorno | Versión recomendada |
|--------|---------------------|
| Python | 3.11+ |
| pip / venv | Incluidos con Python |

---

## Puesta en marcha en local

1. Desde la raíz del monorepo:

   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Crea `.env` a partir de `.env.example` y rellena lo necesario (OAuth, AWS, etc. solo si los usas).

3. Migraciones y servidor:

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

- API: http://127.0.0.1:8000/api/
- Swagger: http://127.0.0.1:8000/swagger/
- ReDoc: http://127.0.0.1:8000/redoc/

---

## Variables de entorno

El fichero **`backend/.env`** (no versionado) se carga automáticamente. Nombres y descripción: **`.env.example`**.

Incluye, entre otras: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`, credenciales **Google OAuth** (`GOOGLE_OAUTH_*`) y, si aplica, **AWS** para S3.

---

## Documentación de la API

Documentación interactiva con **drf-yasg**: **`/swagger/`** y **`/redoc/`**. Existe además un **`api.yaml`** en esta carpeta como referencia.

La API REST usa autenticación por **API key** en la cabecera `Authorization` (ver app `accounts` y `REST_FRAMEWORK` en `ASWproject/settings.py`).

---

## Estructura del proyecto

| Ruta / app | Rol |
|------------|-----|
| `ASWproject/` | Settings, URLs raíz |
| `api/` | Rutas REST bajo `/api/` |
| `news/`, `newest/`, `ask/` | Listados y vistas relacionadas |
| `submissions/`, `comments/`, `threads/` | Envíos, comentarios, hilos |
| `accounts/` | Perfiles, karma, API keys, allauth |
