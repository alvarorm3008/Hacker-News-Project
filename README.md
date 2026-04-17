# ASW — Hacker News (full stack)

Repositorio unificado del **frontend** (React + Vite) y del **backend** (Django REST Framework) del proyecto de *Aplicacions i Serveis Web* (ASW). Trabajo en **grupos de 6 personas**.

## Estructura

| Carpeta | Descripción |
|--------|-------------|
| [`frontend/`](frontend/) | SPA en React que consume la API REST |
| [`backend/`](backend/) | API y lógica de servidor con Django |

## Miembros del grupo (6)

| # | Nombre |
|---|--------|
| 1 | Carla Edo Garzon |
| 2 | Alvaro Rodriguez Martinez |
| 3 | Laia Belaustegui Colilaf |
| 4 | Carla Lopez Campos |
| 5 | *(completa)* |
| 6 | *(completa)* |

## Enlaces útiles

- **Taiga:** [carla172003-hn11a-asw-project](https://tree.taiga.io/project/carla172003-hn11a-asw-project)
- **Frontend desplegado (ejemplo):** https://aswfrontend.onrender.com
- **Backend desplegado (ejemplo):** https://aswproject.onrender.com

## Puesta en marcha rápida

1. **Backend:** sigue [`backend/README.md`](backend/README.md) (Python, migraciones, `runserver`).
2. **Frontend:** sigue [`frontend/README.md`](frontend/README.md) (Node, `npm install`, `npm run dev`).
3. Apunta el frontend a la URL de tu API (local o despliegue) según se indica en el README del frontend.

## Documentación de la API

Con el backend en marcha: **Swagger** en `/swagger/` y **ReDoc** en `/redoc/` (rutas relativas al host del servidor).

## Subir este repo a GitHub (o similar)

En la carpeta raíz `asw-fullstack`:

```bash
git init
git add .
git commit -m "Initial commit: frontend + backend"
git branch -M main
git remote add origin <URL-de-tu-repo-vacio>
git push -u origin main
```

Crea antes un repositorio **vacío** en la plataforma y usa su URL en `git remote add`.
