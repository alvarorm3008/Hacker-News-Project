# Backend — ASW (Django + DRF)

API y aplicación servidor del proyecto tipo **Hacker News**: noticias, envíos, comentarios, hilos, votos y cuentas. Expone una **API REST** bajo el prefijo `/api/` y documentación OpenAPI (Swagger/ReDoc).

**Proyecto en grupo de 6** (ASW). Miembros: Carla Edo Garzon, Alvaro Rodriguez Martinez, Laia Belaustegui Colilaf, Carla Lopez Campos — *añade aquí los nombres 5 y 6*.

## Stack

- **Django** 5.x
- **Django REST Framework**
- **django-cors-headers** (CORS para el frontend)
- **django-allauth** (login social, p. ej. Google)
- **drf-yasg** (Swagger / ReDoc)
- **Almacenamiento:** configuración preparada para **S3** (archivos estáticos/media) en despliegue
- Base de datos por defecto: **SQLite** (`db.sqlite3`) en desarrollo

## Requisitos

- **Python** 3.11+ (recomendado)
- `pip` y entorno virtual (`venv`)

## Instalación y arranque local

```bash
cd backend
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

El servidor queda habitualmente en http://127.0.0.1:8000/

- **API:** http://127.0.0.1:8000/api/
- **Swagger:** http://127.0.0.1:8000/swagger/
- **ReDoc:** http://127.0.0.1:8000/redoc/

## Autenticación API

La API usa autenticación personalizada por **API key** (cabecera `Authorization`). Consulta la implementación en la app `accounts` y la configuración `REST_FRAMEWORK` en `ASWproject/settings.py`.

## CORS

En desarrollo suele estar `CORS_ALLOW_ALL_ORIGINS = True` para facilitar el frontend en otro puerto. En producción conviene restringir orígenes concretos.

## Archivo OpenAPI

En la raíz del backend hay un `api.yaml` de referencia; la documentación interactiva la sirve **drf-yasg** en `/swagger/` y `/redoc/`.

## Despliegue (referencia)

Ejemplo anterior: https://aswproject.onrender.com  

En producción se recomienda usar variables de entorno para `SECRET_KEY`, credenciales de AWS, OAuth de Google y base de datos, en lugar de valores fijados en código.

## Enlaces del proyecto

- **Taiga:** https://tree.taiga.io/project/carla172003-hn11a-asw-project

## Apps Django principales

| App | Rol |
|-----|-----|
| `api` | Rutas REST agregadas bajo `/api/` |
| `news`, `newest`, `ask` | Vistas y flujos de listados |
| `submissions`, `comments`, `threads` | Envíos, comentarios e hilos |
| `accounts` | Usuarios, karma, adaptadores de auth |
